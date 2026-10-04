"""Emit repeatable Figma repairs discovered on 4 October 2026 (no direct network writes)."""
import argparse
import json

NAV_CODE = "await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));const ids=['128:501','128:519','128:537','128:555'];const nodes=await Promise.all(ids.map(id=>figma.getNodeByIdAsync(id)));for(const n of nodes){if(n.name!=='Control'||n.parent.parent.name!=='ProductNavItem')throw Error('Unexpected component');n.strokes=[];}return {mutatedNodeIds:ids,variants:4,remainingStrokes:nodes.map(n=>n.strokes.length)};"

TABS_CODE = "await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));const tabs=figma.currentPage.findAllWithCriteria({types:['FRAME']}).filter(n=>n.name==='Tabs');const size=await figma.variables.getVariableByIdAsync('VariableID:ff1621e75574c9bd13a1bd30974b7816a9e21b86/45334:6');const mutated=[];const evidence=[];for(const tabsNode of tabs){for(const t of tabsNode.findAllWithCriteria({types:['TEXT']}))for(const seg of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(seg.fontName);const segmented=Array.isArray(tabsNode.fills)&&tabsNode.fills.some(p=>p.visible!==false);for(const item of tabsNode.children){if(item.type!=='INSTANCE')continue;const control=item.children.find(n=>n.type==='INSTANCE'&&n.name==='Control');if(!control)continue;item.resize(Math.max(item.width,control.minWidth||0),40);item.layoutSizingVertical='FIXED';item.setBoundVariable('height',size);control.resize(item.width,40);control.layoutSizingHorizontal='FILL';control.layoutSizingVertical='FILL';if(segmented)control.strokes=[];mutated.push(item.id,control.id);evidence.push({id:item.id,w:item.width,h:item.height,controlWidth:control.width,controlHeight:control.height,segmented,strokeCount:control.strokes.length});}}const nav=figma.currentPage.findAllWithCriteria({types:['INSTANCE']}).filter(n=>n.name==='Control'&&n.parent.name==='NavigationItem');const remaining=nav.filter(n=>Array.isArray(n.strokes)&&n.strokes.some(p=>p.visible!==false));for(const n of remaining){n.strokes=[];mutated.push(n.id);}return {mutatedNodeIds:mutated,tabGroups:tabs.length,segmentedGroups:tabs.filter(n=>Array.isArray(n.fills)&&n.fills.some(p=>p.visible!==false)).length,items:evidence,navControls:nav.length,additionalNavOverrides:remaining.length};"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('part', choices=['nav', 'tabs'])
    args = parser.parse_args()
    print(json.dumps({'code': NAV_CODE if args.part == 'nav' else TABS_CODE}))

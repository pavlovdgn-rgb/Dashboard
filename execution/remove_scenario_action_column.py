"""Figma mutation payload: remove duplicate scenario action column at its source."""
import json

CODE = r"""
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const rowSet=await figma.getNodeByIdAsync('135:1062');
const tableSet=await figma.getNodeByIdAsync('136:715');
const removed=[],mutated=[],checks=[];
for(const set of [rowSet,tableSet])for(const t of set.findAllWithCriteria({types:['TEXT']}))for(const segment of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(segment.fontName);
for(const row of rowSet.children){
 const action=row.children.find(n=>n.name==='RowAction');
 if(action){removed.push(action.id);action.remove();mutated.push(row.id);}
 checks.push({id:row.id,columns:row.children.map(n=>n.name),width:row.width});
}
for(const table of tableSet.children){
 const header=table.findOne(n=>n.name==='TableHeader');
 const action=header.children.find(n=>n.name==='Header5');
 if(action){removed.push(action.id);action.remove();mutated.push(header.id);}
 checks.push({id:table.id,headerColumns:header.children.map(n=>n.type==='TEXT'?n.characters:n.name)});
}
rowSet.description='Строка выбора сценария. Выбор радиокнопкой или нажатием на строку; отдельного действия выбора нет. Selected показывает текущий сценарий.';
tableSet.description='Таблица сценариев с пятью столбцами. Выбор радиокнопкой или нажатием на строку обновляет анализ сценария ниже. Столбец «Действие» удалён как дублирующий выбор.';
mutated.push(rowSet.id,tableSet.id);
return {removedNodeIds:removed,mutatedNodeIds:mutated,checks};
"""
if __name__ == '__main__':
    print(json.dumps({'code': CODE}, ensure_ascii=False))

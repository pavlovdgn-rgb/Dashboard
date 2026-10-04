import type { EuiThemeModifications } from '@elastic/eui';
import manifest from './manifest.json';

type Mode='Light'|'Dark';
const tokens=new Map(manifest.tokens.map(token=>[token.css,token]));
function value(css:string,mode:string) {
  const token=tokens.get(css);
  if(!token)throw new Error(`Missing Figma theme token ${css}`);
  return (token.values as Record<string,string>)[mode]??Object.values(token.values)[0];
}
const colorMap:Record<string,string>={
  primary:'brand-primary',accent:'brand-accent',accentSecondary:'brand-success',success:'brand-success',warning:'brand-warning',danger:'brand-danger',
  text:'text-default',title:'text-title',textParagraph:'text-default',textHeading:'text-title',subduedText:'text-subdued',textSubdued:'text-subdued',disabledText:'text-disabled',textDisabled:'text-disabled',
  primaryText:'text-primary',textPrimary:'text-primary',accentText:'text-accent',textAccent:'text-accent',successText:'text-success',textSuccess:'text-success',warningText:'text-warning',textWarning:'text-warning',dangerText:'text-danger',textDanger:'text-danger',
  emptyShade:'shades-empty',lightestShade:'shades-lightest',lightShade:'shades-light',mediumShade:'shades-medium',darkShade:'shades-dark',darkestShade:'shades-darkest',fullShade:'shades-full',
  body:'special-body-aka-page',disabled:'special-disabled',shadow:'special-shadow',
  backgroundBasePlain:'backgrounds-opaque-plain',backgroundBaseSubdued:'backgrounds-opaque-subdued',backgroundBasePrimary:'backgrounds-opaque-primary',backgroundBaseAccent:'backgrounds-opaque-accent',backgroundBaseSuccess:'backgrounds-opaque-success',backgroundBaseWarning:'backgrounds-opaque-warning',backgroundBaseDanger:'backgrounds-opaque-danger',
  backgroundBaseInteractiveSelect:'special-select',borderBaseFormsControl:'form-controls-borders-default',borderBasePlain:'shades-light',
};
const formMap:Record<string,string>={background:'form-controls-backgrounds-default',backgroundDisabled:'form-controls-backgrounds-disabled',backgroundReadOnly:'form-controls-backgrounds-read-only',backgroundFocused:'form-controls-backgrounds-focus',border:'form-controls-borders-default',borderHovered:'form-controls-borders-custom-control',colorDisabled:'text-disabled'};
const buttonMap:Record<string,string>={};
for(const color of ['primary','accent','success','warning','danger','neutral','disabled','risk']){
  const suffix=color[0].toUpperCase()+color.slice(1);
  buttonMap['background'+suffix]='button-default-backgrounds-'+color;
  buttonMap['backgroundFilled'+suffix]='button-filled-backgrounds-'+color;
  buttonMap['textColor'+suffix]='button-default-text-'+color;
  buttonMap['textColorFilled'+suffix]='button-filled-text-'+color;
}
buttonMap.backgroundText='button-default-backgrounds-text';
buttonMap.textColorText='button-default-text-neutral';
function mapValues(mapping:Record<string,string>,mode:Mode){return Object.fromEntries(Object.entries(mapping).map(([key,name])=>[key,value('--elastic-'+name,mode)]));}
export function elasticTheme(scale='medium'):EuiThemeModifications {
  const fontMode=scale==='small'?'Small':scale==='x-small'?'X-small':'Medium';
  const base=parseFloat(value('--size-base','Mode 1'));
  const fontSize=(name:string)=>parseFloat(value('--font-size-'+name,fontMode))/base;
  return {
    base,
    colors:{LIGHT:mapValues(colorMap,'Light'),DARK:mapValues(colorMap,'Dark')},
    font:{family:'Inter, sans-serif',familyCode:'Roboto Mono, monospace',defaultUnits:'px',scale:{xs:fontSize('x-small'),s:fontSize('small'),m:fontSize('medium'),l:fontSize('large'),xl:fontSize('x-large'),xxl:fontSize('xx-large')},title:{weight:'semiBold'}},
    border:{radius:{small:value('--radius-small','Mode 1'),medium:value('--radius-medium','Mode 1')}},
    components:{forms:{LIGHT:mapValues(formMap,'Light'),DARK:mapValues(formMap,'Dark')},buttons:{LIGHT:mapValues(buttonMap,'Light'),DARK:mapValues(buttonMap,'Dark')}},
  };
}

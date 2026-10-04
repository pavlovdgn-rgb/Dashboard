import type { Preview } from '@storybook/react-vite';
import { ThemeFrame } from '../src/storybook/ThemeFrame';
import '../src/icons';
import '../src/fonts';
import '../src/tokens/primitives.css';
import '../src/tokens/semantics.css';
import '../src/tokens/typography.css';
import '../src/global.css';

const preview: Preview = {
  globalTypes: {
    colorMode:{description:'Режим исходной Elastic UI',toolbar:{icon:'circlehollow',items:[{value:'light',title:'Light'},{value:'dark',title:'Dark'}],dynamicTitle:true}},
    typeScale:{description:'Шкала типографики',toolbar:{icon:'paragraph',items:['medium','small','x-small'],dynamicTitle:true}},
  },
  initialGlobals:{colorMode:'light',typeScale:'medium'},
  decorators:[(Story,context)=><ThemeFrame mode={context.globals.colorMode} scale={context.globals.typeScale} product={context.title.startsWith('Components/UX-Lab')||context.title.startsWith('Sandboxes/')}><Story/></ThemeFrame>],
  parameters:{
    layout:'padded', options:{storySort:{order:['Foundation','Components',['UX-Lab','Elastic UI'],'Sandboxes']}}, controls:{expanded:true},
    docs:{source:{type:'dynamic',transform:(_source:string,context:{parameters:Record<string,unknown>;args:Record<string,unknown>})=>{
      const name=context.parameters.exportName;
      if(!name)return _source;
      const args=Object.fromEntries(Object.entries(context.args).filter(([,value])=>typeof value!=='function'&&value!==undefined));
      return `import { ${name} } from './components';\n\n<${name} {...${JSON.stringify(args,null,2)}} />`;
    }}},
    a11y:{test:'todo'},
  },
};
export default preview;

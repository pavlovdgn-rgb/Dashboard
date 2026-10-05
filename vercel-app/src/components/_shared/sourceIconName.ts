import sourceIcons from '../../../ds/icon-source-map.json';
export const iconAliases:Record<string,string>={iInCircle:'info',questionInCircle:'question',cross_in_circle:'crossInCircle',folder_exclamation:'folderExclamation'};
export const sourceIconName=(id:unknown)=>{if(id==='31572:393328')return 'accessibility';if(id==='132:579')return 'bullseye';const name=sourceIcons.find(icon=>icon.id===id)?.name;return name&&!name.includes('=')?(iconAliases[name]||name):undefined;};

import {spawnSync} from 'node:child_process';
import {cpSync,existsSync} from 'node:fs';
import {createRequire} from 'node:module';
import path from 'node:path';

const root=process.cwd();
function run(entry,cwd,args=[]) {
  const require=createRequire(path.join(cwd,'package.json'));
  const executable=entry==='vite/bin/vite.js'?path.join(path.dirname(require.resolve('vite/package.json')),'bin/vite.js'):require.resolve(entry);
  const result=spawnSync(process.execPath,[executable,...args],{cwd,stdio:'inherit'});
  if(result.status!==0)process.exit(result.status||1);
}
for(const cwd of [root,path.join(root,'participant')]) {
  run('typescript/bin/tsc',cwd,['-b']);
  run('vite/bin/vite.js',cwd,['build']);
}
if(!existsSync('participant/dist/index.html'))throw Error('Participant build missing');
cpSync('participant/dist','dist/participant',{recursive:true});
console.log('Dashboard and participant interface built for one Vercel domain.');

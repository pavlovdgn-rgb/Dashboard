import { EuiBreadcrumbs } from '@elastic/eui';
import { useResearch } from '../data/researchStore';
import { useWireRoute } from './useWireRoute';
import s from './WorkspaceBreadcrumbs.module.css';

export function WorkspaceBreadcrumbs() {
  const store=useResearch(),{route}=useWireRoute();
  const breadcrumbs=route.screen==='projects'
    ? [{text:'Все проекты'}]
    : route.screen==='studies'
      ? [{text:'Все проекты',href:'#/projects'},{text:store.project.title}]
      : [{text:'Все проекты',href:'#/projects'},{text:store.project.title,href:'#/studies'},{text:store.study.title}];
  return <EuiBreadcrumbs className={s.root} aria-label="Хлебные крошки" breadcrumbs={breadcrumbs} responsive={false} max={0}/>;
}

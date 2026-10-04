import { useState } from 'react';
import { EuiDataGrid, EuiButtonEmpty, type EuiDataGridColumnSortingConfig, type EuiDataGridStyle } from '@elastic/eui';
import type { VariantValues } from './CatalogComponent';
import { isOn } from './variantValues';
import styles from './ElasticComponent.module.css';

const columns=[{id:'name',displayAsText:'Название'},{id:'type',displayAsText:'Тип'},{id:'count',displayAsText:'Значение',schema:'numeric'}];
const items=Array.from({length:12},(_,index)=>({name:`Элемент ${index+1}`,type:index%2?'Группа Б':'Группа А',count:String(index+1)}));
export function ElasticDataGrid({values:p,index}:{values:VariantValues;index:number}) {
  const [visibleColumns,setVisibleColumns]=useState(columns.map(column=>column.id));
  const [sorting,setSorting]=useState<EuiDataGridColumnSortingConfig[]>([]);
  const [pagination,setPagination]=useState({pageIndex:0,pageSize:5});
  const borders=String(p.Border||p.Borders||'All').toLowerCase() as EuiDataGridStyle['border'];
  const flag=(name:string)=>isOn(Object.entries(p).find(([key])=>key.startsWith(name+'#'))?.[1]);
  const full=index===46;
  const gridStyle:EuiDataGridStyle={border:borders,header:p.Style==='Underline'?'underline':'shade',cellPadding:p.Padding==='Condensed'?'s':p.Padding==='Expanded'?'l':'m',stripes:p['Structured By']==='Row'};
  return <div className={index===42?styles.gridBodyOnly:index===44?styles.gridToolbarOnly:undefined}>
    <EuiDataGrid aria-label="Сетка данных" columns={columns} columnVisibility={{visibleColumns,setVisibleColumns}}
      gridStyle={gridStyle} rowCount={index===43||index===44?0:full?items.length:1}
      toolbarVisibility={index===44?{showColumnSelector:flag('Show columns'),additionalControls:flag('Bulk Actions Button')?<EuiButtonEmpty size="xs">Действия</EuiButtonEmpty>:undefined}:full&&flag('Toolbar')}
      sorting={{columns:sorting,onSort:setSorting}} inMemory={{level:'sorting'}}
      pagination={full&&flag('Pagination')?{...pagination,pageSizeOptions:[5,10],onChangePage:pageIndex=>setPagination(current=>({...current,pageIndex})),onChangeItemsPerPage:pageSize=>setPagination({pageIndex:0,pageSize})}:undefined}
      renderCellValue={({rowIndex,columnId})=>items[rowIndex]?.[columnId as keyof typeof items[number]]??''}/>
  </div>;
}

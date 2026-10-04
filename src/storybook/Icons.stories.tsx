import type { Meta, StoryObj } from '@storybook/react-vite';
import { EuiIcon } from '@elastic/eui';
import { TYPES } from '@elastic/eui/es/components/icon/icon';
import sourceIcons from '../../ds/icon-source-map.json';
import { sourceIconName } from '../components/_shared/sourceIconName';
import { Logo } from '../components';
import styles from './catalog.module.css';

function IconGallery() {
  const icons=sourceIcons.filter(icon=>TYPES.includes(sourceIconName(icon.id)||''));
  return <section className={styles.foundation}><h1>Иконки исходной дизайн-системы</h1><p>Оригинальные SVG Elastic UI. Имена и ключи сверены с Figma. Иконки не перерисованы и не заменены другим набором.</p><div className={styles.icons}><article className={styles.token}><Logo/><strong>UX-Lab · Logo</strong><a href="https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/?node-id=289-13519">Источник Figma</a></article>{icons.map(icon=><article key={icon.id} className={styles.token}><EuiIcon type={sourceIconName(icon.id)!} size="l"/><strong>{icon.name}</strong><code>{icon.id}</code><a href={`https://www.figma.com/design/SNBSKtwsO81j3BdjRGFpAw/?node-id=${icon.id.replace(':','-')}`}>Источник Figma</a></article>)}</div></section>;
}
/** Исходные иконки и утверждённый логотип, с проверяемым происхождением. */
const meta={title:'Foundation/Icons',id:'foundation-icons',component:IconGallery,tags:['autodocs']} satisfies Meta<typeof IconGallery>;
export default meta;
type Story=StoryObj<typeof meta>;
export const Library:Story={};

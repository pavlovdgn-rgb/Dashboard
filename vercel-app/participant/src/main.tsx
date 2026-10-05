import './index.css';
import './cloud/access.css';
import {ensureAccess} from './cloud/access';
void ensureAccess().then(()=>import('./bootstrap'));

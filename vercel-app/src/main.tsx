import './fonts';
import './tokens/primitives.css';
import './tokens/semantics.css';
import './global.css';
import './cloud/access.css';
import {ensureAccess} from './cloud/access';
void ensureAccess().then(()=>import('./bootstrap'));

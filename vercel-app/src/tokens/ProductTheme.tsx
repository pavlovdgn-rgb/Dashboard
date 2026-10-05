import { EuiThemeProvider, type EuiThemeModifications } from '@elastic/eui';
import type { ReactNode } from 'react';
import tokens from './product-theme.json';

// EUI computes contrast colors from concrete token values. Keep this bridge
// generated-data driven, rather than duplicating palette literals in CSS/TS.
const modify:EuiThemeModifications={
  font:{family:'Inter, sans-serif'},
  colors:{LIGHT:{
    primary:tokens['accent/strong'],textPrimary:tokens['accent/strong'],primaryText:tokens['accent/strong'],
    accent:tokens['accent/strong'],success:tokens['status/success/text'],warning:tokens['status/warning/text'],danger:tokens['status/error/text'],
    text:tokens['text/primary'],title:tokens['text/primary'],textParagraph:tokens['text/primary'],subduedText:tokens['text/secondary'],
    emptyShade:tokens['background/surface'],lightestShade:tokens['background/sidebar'],lightShade:tokens['border/subtle'],
    mediumShade:tokens['border/control'],darkShade:tokens['text/secondary'],darkestShade:tokens['text/primary'],
    body:tokens['background/canvas'],
    borderBaseFormsControl:tokens['border/control'],borderBasePlain:tokens['border/subtle'],borderStrongPrimary:tokens['accent/strong'],
    backgroundBasePlain:tokens['background/surface'],backgroundBaseInteractiveSelect:tokens['accent/soft'],backgroundBaseInteractiveHover:tokens['surface/hover'],
  }},
  components:{forms:{LIGHT:{background:tokens['background/surface'],backgroundDisabled:tokens['background/subtle'],backgroundFocused:tokens['background/surface'],border:tokens['border/control'],borderHovered:tokens['accent/strong'],colorDisabled:tokens['text/secondary']}}},
};
export function ProductTheme({children}:{children:ReactNode}) {
  return <EuiThemeProvider colorMode="LIGHT" modify={modify}>{children}</EuiThemeProvider>;
}

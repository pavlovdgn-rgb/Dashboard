"""Replace the obsolete table demo with the reusable interactive renderer."""
from pathlib import Path

root=Path(__file__).resolve().parents[1]
path=root/'src/components/_shared/ProductComponent.tsx'
source=path.read_text(encoding='utf-8')
start=source.index("  if(name==='ParticipantsTable')")
end=source.index("\n  if(name==='FirstClickTargets'||name==='ScenarioTable')",start)
source=source[:start]+"  if(name==='ParticipantsTable')return <ParticipantsTableExample values={p}/>;"+source[end:]
source=source.replace("participantCells(property(p,'ParticipantId','014'))", "<><td>{property(p,'ParticipantId','014')}</td><td>{property(p,'Attempt','1')}</td><td>{outcome()}</td><td>{property(p,'Duration','04:32')}</td><td>{property(p,'SignalCount','4')}</td><td>{coverage()}</td><td>{attempt()}</td></>")
lines=[line for line in source.splitlines() if not line.startswith('  const participantCells=')]
path.write_text('\n'.join(lines)+'\n',encoding='utf-8')

// Shared corgi option definitions, used by both the picker page and the
// image generator so the two can never drift apart.
var C = { o:'#F0A04B', d:'#4A2B16', w:'#FFFFFF', p:'#F7A8C4', t:'#F5859F' };

function ears(sw){
  return `
    <path d="M24,50 Q12,22 20,3 Q36,5 47,32 Z" fill="${C.o}" stroke="${C.d}" stroke-width="${sw}" stroke-linejoin="round"/>
    <path d="M76,50 Q88,22 80,3 Q64,5 53,32 Z" fill="${C.o}" stroke="${C.d}" stroke-width="${sw}" stroke-linejoin="round"/>
    <path d="M29,42 Q21,25 25,13 Q35,18 43,34 Z" fill="${C.p}"/>
    <path d="M71,42 Q79,25 75,13 Q65,18 57,34 Z" fill="${C.p}"/>`;
}
function headShape(sw){
  return `
    <ellipse cx="50" cy="56" rx="33" ry="30" fill="${C.o}" stroke="${C.d}" stroke-width="${sw}"/>
    <path d="M50,28 Q41,38 41,50 Q24,53 22,64 Q26,79 50,79 Q74,79 78,64 Q76,53 59,50 Q59,38 50,28 Z" fill="${C.w}"/>
    <ellipse cx="50" cy="56" rx="33" ry="30" fill="none" stroke="${C.d}" stroke-width="${sw}"/>`;
}
function eyesOpen(){
  return `
    <ellipse cx="36" cy="50" rx="5" ry="5.6" fill="${C.d}"/>
    <ellipse cx="64" cy="50" rx="5" ry="5.6" fill="${C.d}"/>
    <ellipse cx="37.6" cy="48" rx="1.7" ry="1.9" fill="#fff"/>
    <ellipse cx="65.6" cy="48" rx="1.7" ry="1.9" fill="#fff"/>`;
}
function nose(){
  return `<ellipse cx="50" cy="62" rx="7" ry="5.4" fill="${C.d}"/>`;
}
function smile(){
  return `<path d="M50,67 Q50,74 41,73 M50,67 Q50,74 59,73"
      stroke="${C.d}" stroke-width="3.2" fill="none" stroke-linecap="round"/>`;
}
function tongue(){
  return `<path d="M43,71 Q50,84 57,71 Z" fill="${C.t}" stroke="${C.d}" stroke-width="2.4" stroke-linejoin="round"/>`;
}
function cheeks(){
  return `
    <ellipse cx="27" cy="63" rx="6.5" ry="4.4" fill="${C.p}" opacity=".75"/>
    <ellipse cx="73" cy="63" rx="6.5" ry="4.4" fill="${C.p}" opacity=".75"/>`;
}

var CORGIS = [
  { name:'Happy, tongue out', note:'The reference expression — open smile, tongue showing.', svg:
    ears(5) + headShape(5) + eyesOpen() + nose() + tongue() + smile() },

  { name:'Calm smile', note:'Same face, mouth closed. Tidier, a bit more grown-up.', svg:
    ears(5) + headShape(5) + eyesOpen() + nose() + smile() },

  { name:'Winking', note:'One eye shut, tongue out — the cheekiest of the set.', svg:
    ears(5) + headShape(5) +
    `<path d="M31,50 Q36,45 41,50" stroke="${C.d}" stroke-width="3.6" fill="none" stroke-linecap="round"/>
     <ellipse cx="64" cy="50" rx="5" ry="5.6" fill="${C.d}"/>
     <ellipse cx="65.6" cy="48" rx="1.7" ry="1.9" fill="#fff"/>` +
    nose() + tongue() + smile() },

  { name:'Rosy cheeks', note:'Tongue out plus blush — the softest, most storybook.', svg:
    ears(5) + headShape(5) + cheeks() + eyesOpen() + nose() + tongue() + smile() },

  { name:'Bold &amp; chunky', note:'Thicker outline, bigger features — clearest at 12×12.', svg:
    ears(7) +
    `<ellipse cx="50" cy="56" rx="33" ry="30" fill="${C.o}" stroke="${C.d}" stroke-width="7"/>
     <path d="M50,28 Q40,38 40,50 Q23,54 21,65 Q26,80 50,80 Q74,80 79,65 Q77,54 60,50 Q60,38 50,28 Z" fill="${C.w}"/>
     <ellipse cx="50" cy="56" rx="33" ry="30" fill="none" stroke="${C.d}" stroke-width="7"/>
     <ellipse cx="35" cy="50" rx="5.8" ry="6.4" fill="${C.d}"/>
     <ellipse cx="65" cy="50" rx="5.8" ry="6.4" fill="${C.d}"/>
     <ellipse cx="36.8" cy="47.8" rx="2" ry="2.2" fill="#fff"/>
     <ellipse cx="66.8" cy="47.8" rx="2" ry="2.2" fill="#fff"/>
     <ellipse cx="50" cy="63" rx="8" ry="6" fill="${C.d}"/>
     <path d="M42,72 Q50,86 58,72 Z" fill="${C.t}" stroke="${C.d}" stroke-width="2.8" stroke-linejoin="round"/>
     <path d="M50,68.5 Q50,76 40,75 M50,68.5 Q50,76 60,75" stroke="${C.d}" stroke-width="3.6" fill="none" stroke-linecap="round"/>` },

  { name:'Head tilt', note:'Whole head cocked to one side — the most characterful.', svg:
    `<g transform="rotate(-9 50 56)">` +
      ears(5) + headShape(5) + eyesOpen() + nose() + tongue() + smile() +
    `</g>` }
];


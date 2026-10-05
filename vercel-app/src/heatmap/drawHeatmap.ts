import type { ClickPoint } from './types';

/** Accumulate density in an alpha canvas, then apply the product heatmap palette. */
export function drawHeatmap(canvas:HTMLCanvasElement,points:ClickPoint[],width:number,height:number) {
  canvas.width=Math.ceil(width);canvas.height=Math.ceil(height);
  const ctx=canvas.getContext('2d');if(!ctx)return;
  ctx.clearRect(0,0,width,height);if(!points.length)return;
  const pixels=new Float32Array(canvas.width*canvas.height);
  let maximum=0;
  for(const point of points) {
    const x=point.x*width,y=point.y*height,radius=48;
    for(let py=Math.max(0,Math.floor(y-radius));py<Math.min(canvas.height,y+radius);py++) {
      for(let px=Math.max(0,Math.floor(x-radius));px<Math.min(canvas.width,x+radius);px++) {
        const distance=((px-x)**2+(py-y)**2)/(radius*radius);
        if(distance>=1)continue;
        const offset=py*canvas.width+px;
        pixels[offset]+=point.count*Math.exp(-4*distance)*(1-distance);
        maximum=Math.max(maximum,pixels[offset]);
      }
    }
  }
  const image=ctx.createImageData(canvas.width,canvas.height);
  const palette=document.createElement('canvas');palette.width=256;palette.height=1;
  const p=palette.getContext('2d',{willReadFrequently:true});if(!p)return;
  const styles=getComputedStyle(canvas),gradient=p.createLinearGradient(0,0,256,0);
  gradient.addColorStop(0,styles.getPropertyValue('--heatmap-spot-outer').trim());
  gradient.addColorStop(.5,styles.getPropertyValue('--heatmap-spot-middle').trim());
  gradient.addColorStop(1,styles.getPropertyValue('--heatmap-spot-core').trim());
  p.fillStyle=gradient;p.fillRect(0,0,256,1);const colors=p.getImageData(0,0,256,1).data;
  for(let i=0;i<image.data.length;i+=4) {
    const intensity=maximum?pixels[i/4]/maximum:0,offset=Math.round(255*Math.sqrt(intensity))*4;
    image.data[i]=colors[offset];image.data[i+1]=colors[offset+1];image.data[i+2]=colors[offset+2];image.data[i+3]=Math.round(225*Math.pow(intensity,.35));
  }
  ctx.putImageData(image,0,0);
}

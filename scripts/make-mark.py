"""Generates the SystemSerenity SS monogram as filled, tapered SVG paths (public/favicon.svg, public/mark-light.svg, public/mark-dark.svg)."""
import math
def bez(p0,p1,p2,p3,t):
    u=1-t; return (u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0], u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1])
def sample(segs,n=22):
    pts=[]
    for s in segs:
        for i in range(n): pts.append(bez(*s,i/n))
    pts.append(segs[-1][3]); return pts
def outline(pts,wfn):
    L=[];R=[];N=len(pts)
    for i,p in enumerate(pts):
        a=pts[max(i-1,0)]; b=pts[min(i+1,N-1)]
        dx,dy=b[0]-a[0],b[1]-a[1]; d=math.hypot(dx,dy) or 1
        nx,ny=-dy/d,dx/d; w=wfn(i/(N-1),dx/d,dy/d)/2
        L.append((p[0]+nx*w,p[1]+ny*w)); R.append((p[0]-nx*w,p[1]-ny*w))
    poly=L+R[::-1]
    return 'M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in poly)+'Z'
# calligraphic width: thick on down-right diagonal, thin on horizontals, tapered ends
def wf(base,thin,taper_start=0.08,taper_end=0.1,end_w=2.0):
    def f(t,tx,ty):
        bump=math.sin(math.pi*min(max((t-0.05)/0.9,0),1))**1.3
        w=thin+(base-thin)*bump
        if t<taper_start: w=end_w+(w-end_w)*(t/taper_start)
        if t>1-taper_end: w=end_w+(w-end_w)*((1-t)/taper_end)
        return w
    return f
navy=[((76,22),(64,8),(32,10),(31,31)),((31,31),(30,50),(72,50),(70,72)),((70,72),(68,92),(40,94),(28,82))]
teal=[((101,34),(89,20),(58,22),(57,43)),((57,43),(56,62),(98,62),(96,84)),((96,84),(94,106),(56,112),(8,97))]
np_=outline(sample(navy),wf(18,7,0.06,0.1,4))
tp=outline(sample(teal),wf(18,7,0.06,0.4,0.8))
def svg(extra_style,label=True):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 110 118"{' role="img" aria-label="SystemSerenity"' if label else ' aria-hidden="true"'}>
<style>.n{{fill:#0B1F33}}.t{{fill:#2C9C95}}{extra_style}</style>
<path class="t" d="{tp}"/><path class="n" d="{np_}"/></svg>
'''
open('public/favicon.svg','w').write(svg('@media (prefers-color-scheme:dark){.n{fill:#E5E7EB}}'))
open('public/mark-light.svg','w').write(svg(''))
open('public/mark-dark.svg','w').write(svg('.n{fill:#F7F4ED}'))
open('src/components/mark-paths.json','w').write(__import__('json').dumps({'navy':np_,'teal':tp}))
print('ok')

/* ================================================
   Three.js Particle Scene
================================================ */
function initThreeBg(containerId) {
  const el = document.getElementById(containerId)
  if (!el || typeof THREE === 'undefined') return () => {}

  const canvas = document.createElement('canvas')
  canvas.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:0'
  el.style.position = 'relative'
  el.insertBefore(canvas, el.firstChild)

  const W = el.offsetWidth || window.innerWidth
  const H = el.offsetHeight || window.innerHeight

  const scene    = new THREE.Scene()
  const camera   = new THREE.PerspectiveCamera(60, W / H, 1, 3000)
  camera.position.z = 480

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true })
  renderer.setSize(W, H)
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2))

  /* --- Particles --- */
  const N   = 680
  const pos = new Float32Array(N * 3)
  for (let i = 0; i < N; i++) {
    pos[i*3]   = (Math.random() - .5) * 950
    pos[i*3+1] = (Math.random() - .5) * 620
    pos[i*3+2] = (Math.random() - .5) * 380
  }

  const ptGeo = new THREE.BufferGeometry()
  ptGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3))
  const ptMat = new THREE.PointsMaterial({ color: 0xC9A84C, size: 1.8, transparent: true, opacity: .55, sizeAttenuation: true })
  const pts   = new THREE.Points(ptGeo, ptMat)
  scene.add(pts)

  /* --- Connection lines (random pairs) --- */
  const lp = []
  for (let k = 0; k < 200; k++) {
    const a = (Math.random() * N | 0) * 3
    const b = (Math.random() * N | 0) * 3
    lp.push(pos[a], pos[a+1], pos[a+2], pos[b], pos[b+1], pos[b+2])
  }
  const lGeo = new THREE.BufferGeometry()
  lGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(lp), 3))
  const lMat = new THREE.LineBasicMaterial({ color: 0xC9A84C, transparent: true, opacity: .055 })
  const lines = new THREE.LineSegments(lGeo, lMat)
  scene.add(lines)

  /* --- Mouse parallax --- */
  let mx = 0, my = 0
  const onMouse = e => {
    mx = (e.clientX / innerWidth  - .5) * 2
    my = (e.clientY / innerHeight - .5) * 2
  }
  window.addEventListener('mousemove', onMouse, { passive: true })

  /* --- Animation loop --- */
  let alive = true
  let frame;
  (function tick() {
    if (!alive) return
    frame = requestAnimationFrame(tick)
    const t = performance.now() * .0003
    pts.rotation.y   = t * .28
    pts.rotation.x   = t * .14
    lines.rotation.y = pts.rotation.y
    lines.rotation.x = pts.rotation.x

    camera.position.x += (mx * 38 - camera.position.x) * .025
    camera.position.y += (-my * 24 - camera.position.y) * .025
    camera.lookAt(0, 0, 0)

    renderer.render(scene, camera)
  })()

  /* --- Resize --- */
  const onResize = () => {
    const w = el.offsetWidth
    const h = el.offsetHeight
    camera.aspect = w / h
    camera.updateProjectionMatrix()
    renderer.setSize(w, h)
  }
  window.addEventListener('resize', onResize)

  /* --- Visibility pausing --- */
  const obs = new IntersectionObserver(([e]) => {
    alive = e.isIntersecting
    if (alive) { (function tick() { if (!alive) return; frame = requestAnimationFrame(tick); const t = performance.now()*.0003; pts.rotation.y=t*.28; pts.rotation.x=t*.14; lines.rotation.copy(pts.rotation); camera.position.x+=(mx*38-camera.position.x)*.025; camera.position.y+=(-my*24-camera.position.y)*.025; camera.lookAt(0,0,0); renderer.render(scene,camera) })() }
  })
  obs.observe(canvas)

  return () => {
    alive = false
    cancelAnimationFrame(frame)
    window.removeEventListener('mousemove', onMouse)
    window.removeEventListener('resize', onResize)
    obs.disconnect()
    ptGeo.dispose(); ptMat.dispose(); lGeo.dispose(); lMat.dispose()
    renderer.dispose()
  }
}

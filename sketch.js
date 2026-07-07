// Full-page p5.js interaction with the original infinity_logo particle formula.
const PARTICLE_COUNT = 260;
const TRAIL_ALPHA = 28;
const BASE_SPEED = 0.0045;

let particles = [];
let pointerPath = [];
let scaleA;

function setup() {
  const canvas = createCanvas(windowWidth, windowHeight);
  canvas.id('p5-dashboard-canvas');
  pixelDensity(1);
  computeScale();
  for (let i = 0; i < PARTICLE_COUNT; i += 1) {
    particles.push(new Particle(random(TWO_PI)));
  }
  clear();
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
  computeScale();
}

function computeScale() {
  const hero = document.getElementById('hero').getBoundingClientRect();
  const logoRegionWidth = hero.width * 0.44;
  scaleA = min(logoRegionWidth, hero.height) * 0.38;
}

function lemniscate(t, a) {
  const s = sin(t);
  const d = 1 + s * s;
  return {
    x: (a * cos(t)) / d,
    y: (a * s * cos(t)) / d
  };
}

function draw() {
  clear();
  drawPointerLines();

  const hero = document.getElementById('hero').getBoundingClientRect();
  const originX = hero.left + hero.width * 0.78;
  const originY = hero.top + hero.height * 0.5;
  const breath = 0.75 + 0.25 * sin(frameCount * 0.026);

  blendMode(ADD);
  for (const particle of particles) {
    particle.update();
    particle.show(originX, originY, breath);
  }
  blendMode(BLEND);
}

function drawPointerLines() {
  noFill();
  for (let i = pointerPath.length - 1; i > 0; i -= 1) {
    const point = pointerPath[i];
    const previous = pointerPath[i - 1];
    point.life -= 7;
    stroke(232, 189, 72, point.life * 0.62);
    strokeWeight(map(i, 1, pointerPath.length, 0.7, 2.5));
    line(previous.x, previous.y, point.x, point.y);
    if (point.life <= 0) pointerPath.splice(i, 1);
  }
}

function mouseMoved() {
  pointerPath.push({ x: mouseX, y: mouseY, life: 255 });
  if (pointerPath.length > 44) pointerPath.shift();
  return false;
}

function touchMoved() {
  pointerPath.push({ x: mouseX, y: mouseY, life: 255 });
  if (pointerPath.length > 44) pointerPath.shift();
  return false;
}

class Particle {
  constructor(t) {
    this.t = t;
    this.speed = BASE_SPEED * random(0.6, 1.5);
    this.size = random(1.2, 3.4);
    this.offset = random(-6, 6);
    this.offsetAngle = random(TWO_PI);
    this.col = color(
      random(212, 255),
      random(160, 205),
      random(20, 80)
    );
  }

  update() {
    this.t += this.speed;
    if (this.t > TWO_PI) this.t -= TWO_PI;
    this.offsetAngle += 0.01;
  }

  show(originX, originY, breath) {
    const pos = lemniscate(this.t, scaleA);
    const x = originX + pos.x + this.offset * cos(this.offsetAngle);
    const y = originY + pos.y + this.offset * sin(this.offsetAngle) * 0.6;

    noStroke();
    fill(red(this.col), green(this.col), blue(this.col), 22 * 0.8 * breath);
    circle(x, y, this.size * 5);
    fill(red(this.col), green(this.col), blue(this.col), 190 * 0.8 * breath);
    circle(x, y, this.size);
  }
}

// Set up the scene, camera, and renderer

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();

renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Create a cube and add it to the scene
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshBasicMaterial({ color: 0x333333 });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

const vertices = [
  // Front face
  new THREE.Vector3(-1, 1, 1),
  new THREE.Vector3(1, 1, 1),
  new THREE.Vector3(1, -1, 1),
  new THREE.Vector3(-1, -1, 1),
  // Back face
  new THREE.Vector3(-1, 1, -1),
  new THREE.Vector3(1, 1, -1),
  new THREE.Vector3(1, -1, -1),
  new THREE.Vector3(-1, -1, -1),
  // Connections between front and back faces
  new THREE.Vector3(-1, 1, 1),
  new THREE.Vector3(-1, 1, -1),
  new THREE.Vector3(1, 1, 1),
  new THREE.Vector3(1, 1, -1),
  new THREE.Vector3(1, -1, 1),
  new THREE.Vector3(1, -1, -1),
  new THREE.Vector3(-1, -1, 1),
  new THREE.Vector3(-1, -1, -1)
];

// Create the wireframe using the LineSegments class
const wireframeGeometry = new THREE.BufferGeometry().setFromPoints(vertices);
const wireframeMaterial = new THREE.LineBasicMaterial({ color: 0xffffff });
const wireframe = new THREE.LineSegments(wireframeGeometry, wireframeMaterial);
scene.add(wireframe);

// Position the camera and render the scene
camera.position.z = 5;
renderer.render(scene, camera);

// Animate the cube and wireframe
function animate() {
  requestAnimationFrame(animate);

  // Rotate the cube and wireframe
  cube.rotation.x += 0.01;
  cube.rotation.y += 0.01;
  wireframe.rotation.x -= .02;
  wireframe.rotation.y -= .02;

  // Render the scene
  renderer.render(scene, camera);
}

animate();
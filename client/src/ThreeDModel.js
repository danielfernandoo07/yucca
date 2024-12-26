import React, { useEffect, useRef } from "react";
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";

const ThreeDModel = ({ responseText }) => {
  const mountRef = useRef(null);

  useEffect(() => {
    // Setup Three.js scene
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    mountRef.current.appendChild(renderer.domElement);

    // Add light
    const light = new THREE.AmbientLight(0xffffff, 1);
    scene.add(light);

    // Load 3D model
    const loader = new GLTFLoader();
    let model;
    loader.load(
      "/models/person.glb",
      (gltf) => {
        model = gltf.scene;
        scene.add(model);
        model.position.set(0, -1, 0);
      },
      undefined,
      (error) => {
        console.error(error);
      }
    );

    camera.position.z = 5;

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      renderer.render(scene, camera);
    };
    animate();

    // Cleanup
    return () => {
      mountRef.current.removeChild(renderer.domElement);
    };
  }, []);

  useEffect(() => {
    // Trigger animation on responseText change
    if (responseText) {
      console.log("Animating based on response:", responseText);
      // Add animation logic here
    }
  }, [responseText]);

  return <div ref={mountRef}></div>;
};

export default ThreeDModel;

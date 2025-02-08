import { useEffect, useState } from "react";
import Particles, { initParticlesEngine } from "@tsparticles/react";
import { loadFull } from "tsparticles";

export default function Particle() {
    const [init, setInit] = useState(false);

    useEffect(() => {
        initParticlesEngine(async (engine) => {
            await loadFull(engine);
        }).then(() => setInit(true));
    }, []);

    return (
        <div className="particles-background">
            {init && (
                <Particles
                    id="tsparticles"
                    options={{
                        fullScreen: { enable: true, zIndex: -1 },
                        background: { color: "#EEEEEE" },
                        fpsLimit: 60,
                        interactivity: {
                            events: {
                                onHover: { enable: true, mode: "bubble" },
                                onClick: { enable: true, mode: "repulse" },
                                resize: true,
                            },
                            modes: {
                                repulse: { distance: 100, duration: 1.5 },
                                bubble: { distance: 200, size: 10, duration: 2, opacity: 0.8 },
                            },
                        },
                        particles: {
                            color: {
                                value: ["#228B22", "#6A994E", "#A7C957", "#38A3A5"],
                                animation: { enable: true, speed: 5, sync: false },
                            },
                            links: {
                                color: "#4CAF50",
                                distance: 120,
                                enable: true,
                                opacity: 0.7,
                                width: 1,
                            },
                            move: {
                                enable: true,
                                speed: 1.5,
                                outModes: { default: "out" },
                                random: true,
                            },
                            number: {
                                density: { enable: true, area: 900 },
                                value: 120,
                            },
                            opacity: {
                                value: 0.8,
                                random: true,
                                animation: { enable: true, speed: 0.5, sync: false },
                            },
                            size: {
                                value: { min: 2, max: 5 },
                                random: true,
                                animation: { enable: true, speed: 3, sync: false },
                            },
                            shape: { type: "circle" },
                        },
                        detectRetina: true,
                    }}
                />
            )}
        </div>
    );
}
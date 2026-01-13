import { useEffect, useRef, useState } from 'react';

interface VantaBackgroundProps {
  className?: string;
  color?: number;
  points?: number;
  maxDistance?: number;
  spacing?: number;
}

export default function VantaBackground({
  className = 'vanta-background',
  color = 0x134a52,
  points = 10.0,
  maxDistance = 20.0,
  spacing = 16.0,
}: VantaBackgroundProps): JSX.Element {
  const vantaRef = useRef<HTMLDivElement>(null);
  const [vantaEffect, setVantaEffect] = useState<any>(null);

  useEffect(() => {
    // Only run on client side
    if (typeof window === 'undefined') return;

    const loadVanta = async () => {
      try {
        const THREE = await import('three');
        const NET = await import('vanta/dist/vanta.net.min');

        if (!vantaEffect && vantaRef.current) {
          setVantaEffect(
            NET.default({
              el: vantaRef.current,
              THREE,
              mouseControls: true,
              touchControls: true,
              minHeight: 200.0,
              minWidth: 200.0,
              scale: 1.0,
              scaleMobile: 1.0,
              color,
              backgroundColor: 0x0e1114,
              points,
              maxDistance,
              spacing,
              gyroControls: false,
              speed: 0.5,
            })
          );
        }
      } catch (error) {
        console.error('Failed to load Vanta.js:', error);
      }
    };

    loadVanta();

    return () => {
      if (vantaEffect) {
        vantaEffect.destroy();
      }
    };
  }, [vantaEffect, color, points, maxDistance, spacing]);

  return <div ref={vantaRef} className={className} />;
}

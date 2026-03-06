"use client";

import { useState, useEffect, useRef } from "react";
import { motion, useInView, useSpring } from "framer-motion";

interface AnimatedCounterProps {
  value: number;
  prefix?: string;
  suffix?: string;
  className?: string;
}

export default function AnimatedCounter({
  value,
  prefix = "",
  suffix = "",
  className = "",
}: AnimatedCounterProps) {
  const ref = useRef<HTMLSpanElement>(null);
  const isInView = useInView(ref, { once: true, margin: "-50px" });
  const [displayValue, setDisplayValue] = useState(0);

  // Spring animation for smooth counting
  const spring = useSpring(0, {
    stiffness: 60,
    damping: 20,
    mass: 1,
  });

  useEffect(() => {
    if (isInView) {
      spring.set(value);
    }
  }, [isInView, value, spring]);

  // Update state when spring value changes
  useEffect(() => {
    const unsubscribe = spring.on("change", (latestValue) => {
      setDisplayValue(Math.round(latestValue));
    });
    return () => unsubscribe();
  }, [spring]);

  return (
    <span className={className}>
      <motion.span ref={ref} className="tabular-nums">
        {prefix}
        {displayValue}
        {suffix}
      </motion.span>
    </span>
  );
}

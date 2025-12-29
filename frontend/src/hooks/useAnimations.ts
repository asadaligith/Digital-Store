/**
 * Custom hook providing GSAP animation utilities.
 *
 * Features:
 * - GPU-accelerated animations (transform and opacity only)
 * - Fade in/out animations
 * - Slide animations (up, down, left, right)
 * - Scale animations
 * - Stagger animations for lists
 * - Page transition animations
 * - Automatic cleanup on unmount
 * - TypeScript support
 *
 * Performance Guidelines:
 * - Only animate transform (translateX/Y/Z, scale, rotate) and opacity
 * - Avoid animating layout properties (width, height, margin, padding)
 * - Use will-change CSS property sparingly
 * - Clean up animations on unmount
 */

import { useEffect, useRef } from 'react';
import gsap from 'gsap';

export interface AnimationOptions {
  /** Animation duration in seconds */
  duration?: number;

  /** Animation delay in seconds */
  delay?: number;

  /** GSAP easing function */
  ease?: string;

  /** Stagger time for multiple elements (in seconds) */
  stagger?: number;

  /** Callback when animation completes */
  onComplete?: () => void;
}

export interface SlideOptions extends AnimationOptions {
  /** Slide direction */
  direction?: 'up' | 'down' | 'left' | 'right';

  /** Slide distance in pixels */
  distance?: number;
}

export interface StaggerOptions extends AnimationOptions {
  /** Stagger direction */
  from?: 'start' | 'end' | 'center' | 'edges';
}

/**
 * Hook providing GSAP animation utilities with automatic cleanup.
 *
 * @example
 * ```tsx
 * const { fadeIn, slideIn, scaleIn, staggerIn } = useAnimations();
 *
 * useEffect(() => {
 *   fadeIn('.product-card', { duration: 0.5, stagger: 0.1 });
 * }, [fadeIn]);
 * ```
 */
export const useAnimations = () => {
  const animationsRef = useRef<gsap.core.Tween[]>([]);

  // Cleanup all animations on unmount
  useEffect(() => {
    return () => {
      animationsRef.current.forEach((animation) => {
        animation.kill();
      });
      animationsRef.current = [];
    };
  }, []);

  /**
   * Fade in animation.
   */
  const fadeIn = (
    target: gsap.TweenTarget,
    options: AnimationOptions = {}
  ) => {
    const {
      duration = 0.5,
      delay = 0,
      ease = 'power2.out',
      stagger = 0,
      onComplete,
    } = options;

    const animation = gsap.fromTo(
      target,
      { opacity: 0 },
      {
        opacity: 1,
        duration,
        delay,
        ease,
        stagger,
        onComplete,
      }
    );

    animationsRef.current.push(animation);
    return animation;
  };

  /**
   * Fade out animation.
   */
  const fadeOut = (
    target: gsap.TweenTarget,
    options: AnimationOptions = {}
  ) => {
    const {
      duration = 0.5,
      delay = 0,
      ease = 'power2.in',
      stagger = 0,
      onComplete,
    } = options;

    const animation = gsap.to(target, {
      opacity: 0,
      duration,
      delay,
      ease,
      stagger,
      onComplete,
    });

    animationsRef.current.push(animation);
    return animation;
  };

  /**
   * Slide in animation.
   */
  const slideIn = (
    target: gsap.TweenTarget,
    options: SlideOptions = {}
  ) => {
    const {
      direction = 'up',
      distance = 50,
      duration = 0.6,
      delay = 0,
      ease = 'power2.out',
      stagger = 0,
      onComplete,
    } = options;

    const fromVars: gsap.TweenVars = { opacity: 0 };
    const toVars: gsap.TweenVars = {
      opacity: 1,
      duration,
      delay,
      ease,
      stagger,
      onComplete,
    };

    // Set initial position based on direction
    switch (direction) {
      case 'up':
        fromVars.y = distance;
        toVars.y = 0;
        break;
      case 'down':
        fromVars.y = -distance;
        toVars.y = 0;
        break;
      case 'left':
        fromVars.x = distance;
        toVars.x = 0;
        break;
      case 'right':
        fromVars.x = -distance;
        toVars.x = 0;
        break;
    }

    const animation = gsap.fromTo(target, fromVars, toVars);

    animationsRef.current.push(animation);
    return animation;
  };

  /**
   * Slide out animation.
   */
  const slideOut = (
    target: gsap.TweenTarget,
    options: SlideOptions = {}
  ) => {
    const {
      direction = 'down',
      distance = 50,
      duration = 0.6,
      delay = 0,
      ease = 'power2.in',
      stagger = 0,
      onComplete,
    } = options;

    const toVars: gsap.TweenVars = {
      opacity: 0,
      duration,
      delay,
      ease,
      stagger,
      onComplete,
    };

    // Set final position based on direction
    switch (direction) {
      case 'up':
        toVars.y = -distance;
        break;
      case 'down':
        toVars.y = distance;
        break;
      case 'left':
        toVars.x = -distance;
        break;
      case 'right':
        toVars.x = distance;
        break;
    }

    const animation = gsap.to(target, toVars);

    animationsRef.current.push(animation);
    return animation;
  };

  /**
   * Scale in animation (zoom in effect).
   */
  const scaleIn = (
    target: gsap.TweenTarget,
    options: AnimationOptions = {}
  ) => {
    const {
      duration = 0.5,
      delay = 0,
      ease = 'back.out(1.2)',
      stagger = 0,
      onComplete,
    } = options;

    const animation = gsap.fromTo(
      target,
      { opacity: 0, scale: 0.8 },
      {
        opacity: 1,
        scale: 1,
        duration,
        delay,
        ease,
        stagger,
        onComplete,
      }
    );

    animationsRef.current.push(animation);
    return animation;
  };

  /**
   * Scale out animation (zoom out effect).
   */
  const scaleOut = (
    target: gsap.TweenTarget,
    options: AnimationOptions = {}
  ) => {
    const {
      duration = 0.5,
      delay = 0,
      ease = 'back.in(1.2)',
      stagger = 0,
      onComplete,
    } = options;

    const animation = gsap.to(target, {
      opacity: 0,
      scale: 0.8,
      duration,
      delay,
      ease,
      stagger,
      onComplete,
    });

    animationsRef.current.push(animation);
    return animation;
  };

  /**
   * Stagger in animation for lists.
   */
  const staggerIn = (
    target: gsap.TweenTarget,
    options: StaggerOptions = {}
  ) => {
    const {
      duration = 0.6,
      delay = 0,
      ease = 'power2.out',
      stagger = 0.1,
      from = 'start',
      onComplete,
    } = options;

    const animation = gsap.fromTo(
      target,
      { opacity: 0, y: 30 },
      {
        opacity: 1,
        y: 0,
        duration,
        delay,
        ease,
        stagger: {
          amount: stagger,
          from,
        },
        onComplete,
      }
    );

    animationsRef.current.push(animation);
    return animation;
  };

  /**
   * Page transition in animation.
   */
  const pageIn = (target: gsap.TweenTarget) => {
    return slideIn(target, {
      direction: 'up',
      distance: 30,
      duration: 0.8,
      ease: 'power3.out',
    });
  };

  /**
   * Page transition out animation.
   */
  const pageOut = (target: gsap.TweenTarget) => {
    return fadeOut(target, {
      duration: 0.4,
      ease: 'power2.in',
    });
  };

  /**
   * Product card hover animation.
   */
  const cardHover = (target: gsap.TweenTarget, isHovering: boolean) => {
    const animation = gsap.to(target, {
      y: isHovering ? -8 : 0,
      scale: isHovering ? 1.02 : 1,
      duration: 0.3,
      ease: 'power2.out',
    });

    animationsRef.current.push(animation);
    return animation;
  };

  /**
   * Cart item add animation.
   */
  const cartItemAdd = (target: gsap.TweenTarget) => {
    return gsap.fromTo(
      target,
      { opacity: 0, x: 50, scale: 0.8 },
      {
        opacity: 1,
        x: 0,
        scale: 1,
        duration: 0.5,
        ease: 'back.out(1.4)',
      }
    );
  };

  /**
   * Cart item remove animation.
   */
  const cartItemRemove = (target: gsap.TweenTarget) => {
    return gsap.to(target, {
      opacity: 0,
      x: -50,
      height: 0,
      marginBottom: 0,
      duration: 0.4,
      ease: 'power2.in',
    });
  };

  /**
   * Shake animation (for errors or validation).
   */
  const shake = (target: gsap.TweenTarget) => {
    const animation = gsap.fromTo(
      target,
      { x: -10 },
      {
        x: 10,
        repeat: 3,
        yoyo: true,
        duration: 0.1,
        ease: 'power2.inOut',
      }
    );

    animationsRef.current.push(animation);
    return animation;
  };

  /**
   * Pulse animation (for attention).
   */
  const pulse = (target: gsap.TweenTarget, loops: number = 2) => {
    const animation = gsap.fromTo(
      target,
      { scale: 1 },
      {
        scale: 1.05,
        repeat: loops * 2 - 1,
        yoyo: true,
        duration: 0.3,
        ease: 'power2.inOut',
      }
    );

    animationsRef.current.push(animation);
    return animation;
  };

  return {
    fadeIn,
    fadeOut,
    slideIn,
    slideOut,
    scaleIn,
    scaleOut,
    staggerIn,
    pageIn,
    pageOut,
    cardHover,
    cartItemAdd,
    cartItemRemove,
    shake,
    pulse,
  };
};

export default useAnimations;

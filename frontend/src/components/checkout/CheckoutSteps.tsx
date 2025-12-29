/**
 * CheckoutSteps Component
 *
 * Progress indicator for multi-step checkout wizard.
 * Shows current step and allows navigation to completed steps.
 */

import React from 'react';
import { CheckoutStep } from '../../types/address';

interface CheckoutStepsProps {
  currentStep: CheckoutStep;
  onStepClick?: (step: CheckoutStep) => void;
  completedSteps?: CheckoutStep[];
}

const STEPS = [
  {
    id: CheckoutStep.SHIPPING_INFO,
    label: 'Shipping',
    shortLabel: 'Ship',
  },
  {
    id: CheckoutStep.SHIPPING_METHOD,
    label: 'Method',
    shortLabel: 'Method',
  },
  {
    id: CheckoutStep.REVIEW,
    label: 'Review',
    shortLabel: 'Review',
  },
  {
    id: CheckoutStep.PAYMENT,
    label: 'Payment',
    shortLabel: 'Pay',
  },
];

export const CheckoutSteps: React.FC<CheckoutStepsProps> = ({
  currentStep,
  onStepClick,
  completedSteps = [],
}) => {
  const currentStepIndex = STEPS.findIndex((step) => step.id === currentStep);

  const isStepCompleted = (stepId: CheckoutStep): boolean => {
    return completedSteps.includes(stepId);
  };

  const isStepActive = (stepId: CheckoutStep): boolean => {
    return stepId === currentStep;
  };

  const canClickStep = (stepId: CheckoutStep): boolean => {
    return isStepCompleted(stepId) && onStepClick !== undefined;
  };

  return (
    <div className="w-full py-6">
      {/* Desktop Steps */}
      <div className="hidden md:flex items-center justify-between">
        {STEPS.map((step, index) => {
          const isCompleted = isStepCompleted(step.id);
          const isActive = isStepActive(step.id);
          const isClickable = canClickStep(step.id);

          return (
            <React.Fragment key={step.id}>
              {/* Step */}
              <div className="flex items-center">
                <button
                  onClick={() => isClickable && onStepClick?.(step.id)}
                  disabled={!isClickable}
                  className={`flex items-center gap-3 ${
                    isClickable ? 'cursor-pointer' : 'cursor-default'
                  }`}
                >
                  {/* Step Number */}
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-colors ${
                      isActive
                        ? 'bg-primary-600 text-white'
                        : isCompleted
                        ? 'bg-green-600 text-white'
                        : 'bg-gray-200 text-gray-600'
                    }`}
                  >
                    {isCompleted ? (
                      <svg
                        className="w-6 h-6"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                    ) : (
                      index + 1
                    )}
                  </div>

                  {/* Step Label */}
                  <div
                    className={`text-sm font-medium ${
                      isActive
                        ? 'text-primary-600'
                        : isCompleted
                        ? 'text-green-600'
                        : 'text-gray-500'
                    }`}
                  >
                    {step.label}
                  </div>
                </button>
              </div>

              {/* Connector Line */}
              {index < STEPS.length - 1 && (
                <div className="flex-1 h-0.5 mx-4 bg-gray-200">
                  <div
                    className={`h-full transition-all ${
                      index < currentStepIndex ? 'bg-green-600' : 'bg-gray-200'
                    }`}
                    style={{
                      width: index < currentStepIndex ? '100%' : '0%',
                    }}
                  ></div>
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>

      {/* Mobile Steps */}
      <div className="md:hidden">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-600">
            Step {currentStepIndex + 1} of {STEPS.length}
          </span>
          <span className="text-sm font-medium text-primary-600">
            {STEPS[currentStepIndex].label}
          </span>
        </div>

        {/* Progress Bar */}
        <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
          <div
            className="h-full bg-primary-600 transition-all duration-300"
            style={{
              width: `${((currentStepIndex + 1) / STEPS.length) * 100}%`,
            }}
          ></div>
        </div>

        {/* Step Indicators */}
        <div className="flex justify-between mt-3">
          {STEPS.map((step, index) => (
            <div
              key={step.id}
              className={`text-xs ${
                index === currentStepIndex
                  ? 'text-primary-600 font-medium'
                  : index < currentStepIndex
                  ? 'text-green-600'
                  : 'text-gray-400'
              }`}
            >
              {step.shortLabel}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

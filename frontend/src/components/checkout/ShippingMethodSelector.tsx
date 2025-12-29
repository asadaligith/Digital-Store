/**
 * ShippingMethodSelector Component
 *
 * Radio button group for selecting shipping method.
 * Displays cost and estimated delivery for each option.
 */

import React, { useState, useEffect } from 'react';
import { Button } from '../common/Button';
import { Spinner } from '../common/Spinner';
import { ShippingMethod } from '../../types/address';

interface ShippingMethodSelectorProps {
  methods: ShippingMethod[];
  selectedMethod: ShippingMethod | null;
  onSelect: (method: ShippingMethod) => void;
  onContinue: () => void;
  onBack: () => void;
  isLoading?: boolean;
}

export const ShippingMethodSelector: React.FC<ShippingMethodSelectorProps> = ({
  methods,
  selectedMethod,
  onSelect,
  onContinue,
  onBack,
  isLoading = false,
}) => {
  const [selected, setSelected] = useState<string | null>(
    selectedMethod?.method || null
  );

  useEffect(() => {
    if (selectedMethod) {
      setSelected(selectedMethod.method);
    }
  }, [selectedMethod]);

  const handleSelect = (method: ShippingMethod) => {
    setSelected(method.method);
    onSelect(method);
  };

  const handleContinue = () => {
    if (selected) {
      onContinue();
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Shipping Method</h2>
        <p className="text-gray-600">Choose your preferred shipping option</p>
      </div>

      {/* Shipping Methods */}
      <div className="space-y-3">
        {methods.map((method) => (
          <button
            key={method.method}
            type="button"
            onClick={() => handleSelect(method)}
            className={`w-full p-4 border-2 rounded-lg text-left transition-all ${
              selected === method.method
                ? 'border-primary-600 bg-primary-50'
                : 'border-gray-200 hover:border-gray-300 bg-white'
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex items-start gap-3">
                {/* Radio Button */}
                <div className="mt-1">
                  <div
                    className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                      selected === method.method
                        ? 'border-primary-600'
                        : 'border-gray-300'
                    }`}
                  >
                    {selected === method.method && (
                      <div className="w-3 h-3 rounded-full bg-primary-600"></div>
                    )}
                  </div>
                </div>

                {/* Method Info */}
                <div className="flex-1">
                  <div className="font-semibold text-gray-900">{method.name}</div>
                  <div className="text-sm text-gray-600 mt-1">
                    {method.description}
                  </div>
                  <div className="text-sm text-gray-500 mt-1">
                    Estimated delivery: {method.estimated_days}{' '}
                    {method.estimated_days === 1 ? 'day' : 'days'}
                  </div>
                </div>
              </div>

              {/* Price */}
              <div className="ml-4">
                <div className="font-bold text-gray-900">
                  {method.cost === 0 ? (
                    <span className="text-green-600">FREE</span>
                  ) : (
                    `$${method.cost.toFixed(2)}`
                  )}
                </div>
              </div>
            </div>
          </button>
        ))}
      </div>

      {/* Actions */}
      <div className="flex gap-4 pt-4">
        <Button type="button" variant="outline" onClick={onBack}>
          Back
        </Button>
        <Button
          type="button"
          variant="primary"
          onClick={handleContinue}
          disabled={!selected}
          fullWidth
        >
          Continue to Review
        </Button>
      </div>
    </div>
  );
};

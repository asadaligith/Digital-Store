/**
 * Checkout Context
 *
 * Provides checkout state and actions for the multi-step checkout wizard.
 * Manages shipping address, shipping method, totals, and step navigation.
 */

import React, { createContext, useContext, useState, useCallback } from 'react';
import {
  Address,
  AddressType,
  ShippingMethod,
  ShippingMethodType,
  CheckoutStep,
  OrderPreview,
  CheckoutTotals,
} from '../types/address';
import {
  validateCart as validateCartAPI,
  getShippingMethods as getShippingMethodsAPI,
  createOrderPreview as createOrderPreviewAPI,
} from '../services/api/checkout';

// ===== Types =====

interface CheckoutContextValue {
  // State
  currentStep: CheckoutStep;
  shippingAddress: Partial<Address> | null;
  shippingMethod: ShippingMethod | null;
  orderPreview: OrderPreview | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  setCurrentStep: (step: CheckoutStep) => void;
  setShippingAddress: (address: Partial<Address>) => void;
  setShippingMethod: (method: ShippingMethod) => void;
  nextStep: () => void;
  previousStep: () => void;
  goToStep: (step: CheckoutStep) => void;
  validateAndProceed: (cartId: string) => Promise<boolean>;
  loadShippingMethods: () => Promise<ShippingMethod[]>;
  createPreview: (cartId: string) => Promise<void>;
  resetCheckout: () => void;
}

// ===== Context =====

const CheckoutContext = createContext<CheckoutContextValue | undefined>(undefined);

// ===== Provider =====

interface CheckoutProviderProps {
  children: React.ReactNode;
}

export const CheckoutProvider: React.FC<CheckoutProviderProps> = ({ children }) => {
  const [currentStep, setCurrentStep] = useState<CheckoutStep>(CheckoutStep.SHIPPING_INFO);
  const [shippingAddress, setShippingAddress] = useState<Partial<Address> | null>(null);
  const [shippingMethod, setShippingMethod] = useState<ShippingMethod | null>(null);
  const [orderPreview, setOrderPreview] = useState<OrderPreview | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Move to next step
   */
  const nextStep = useCallback(() => {
    const steps = Object.values(CheckoutStep);
    const currentIndex = steps.indexOf(currentStep);

    if (currentIndex < steps.length - 1) {
      setCurrentStep(steps[currentIndex + 1]);
    }
  }, [currentStep]);

  /**
   * Move to previous step
   */
  const previousStep = useCallback(() => {
    const steps = Object.values(CheckoutStep);
    const currentIndex = steps.indexOf(currentStep);

    if (currentIndex > 0) {
      setCurrentStep(steps[currentIndex - 1]);
    }
  }, [currentStep]);

  /**
   * Go to specific step
   */
  const goToStep = useCallback((step: CheckoutStep) => {
    setCurrentStep(step);
  }, []);

  /**
   * Validate cart and proceed
   */
  const validateAndProceed = useCallback(async (cartId: string): Promise<boolean> => {
    try {
      setIsLoading(true);
      setError(null);

      const validation = await validateCartAPI(cartId);

      if (!validation.valid) {
        setError(validation.errors.join(', '));
        return false;
      }

      return true;
    } catch (err: any) {
      console.error('Cart validation failed:', err);
      setError(err.response?.data?.message || 'Failed to validate cart');
      return false;
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Load available shipping methods
   */
  const loadShippingMethods = useCallback(async (): Promise<ShippingMethod[]> => {
    try {
      setIsLoading(true);
      setError(null);

      const methods = await getShippingMethodsAPI();
      return methods;
    } catch (err: any) {
      console.error('Failed to load shipping methods:', err);
      setError(err.response?.data?.message || 'Failed to load shipping methods');
      return [];
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Create order preview
   */
  const createPreview = useCallback(
    async (cartId: string) => {
      if (!shippingAddress || !shippingMethod) {
        setError('Shipping address and method are required');
        return;
      }

      try {
        setIsLoading(true);
        setError(null);

        // Prepare address data
        const addressData: Omit<Address, '_id' | 'user_id'> = {
          type: AddressType.SHIPPING,
          full_name: shippingAddress.full_name || '',
          address_line1: shippingAddress.address_line1 || '',
          address_line2: shippingAddress.address_line2,
          city: shippingAddress.city || '',
          state: shippingAddress.state || '',
          postal_code: shippingAddress.postal_code || '',
          country: shippingAddress.country || 'US',
          phone: shippingAddress.phone || '',
          is_default: false,
        };

        const preview = await createOrderPreviewAPI(
          cartId,
          addressData,
          shippingMethod.method
        );

        setOrderPreview(preview);

        if (!preview.can_proceed) {
          setError(preview.validation_errors.join(', '));
        }
      } catch (err: any) {
        console.error('Failed to create order preview:', err);
        setError(err.response?.data?.message || 'Failed to create order preview');
      } finally {
        setIsLoading(false);
      }
    },
    [shippingAddress, shippingMethod]
  );

  /**
   * Reset checkout state
   */
  const resetCheckout = useCallback(() => {
    setCurrentStep(CheckoutStep.SHIPPING_INFO);
    setShippingAddress(null);
    setShippingMethod(null);
    setOrderPreview(null);
    setError(null);
  }, []);

  const value: CheckoutContextValue = {
    currentStep,
    shippingAddress,
    shippingMethod,
    orderPreview,
    isLoading,
    error,
    setCurrentStep,
    setShippingAddress,
    setShippingMethod,
    nextStep,
    previousStep,
    goToStep,
    validateAndProceed,
    loadShippingMethods,
    createPreview,
    resetCheckout,
  };

  return <CheckoutContext.Provider value={value}>{children}</CheckoutContext.Provider>;
};

// ===== Hook =====

/**
 * Hook to access checkout context
 *
 * @throws Error if used outside CheckoutProvider
 */
export const useCheckout = () => {
  const context = useContext(CheckoutContext);

  if (context === undefined) {
    throw new Error('useCheckout must be used within a CheckoutProvider');
  }

  return context;
};

/**
 * Checkout Page
 *
 * Multi-step checkout wizard:
 * 1. Shipping Information
 * 2. Shipping Method
 * 3. Order Review
 * 4. Payment (to be implemented in Phase 6)
 */

import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';
import { useCheckout } from '../contexts/CheckoutContext';
import { CheckoutStep, Address, ShippingMethod } from '../types/address';
import { ShippingForm } from '../components/checkout/ShippingForm';
import { ShippingMethodSelector } from '../components/checkout/ShippingMethodSelector';
import { OrderReview } from '../components/checkout/OrderReview';
import { CheckoutSteps } from '../components/checkout/CheckoutSteps';
import { Spinner } from '../components/common/Spinner';

export const Checkout: React.FC = () => {
  const navigate = useNavigate();
  const { cart, fetchCart } = useCart();
  const {
    currentStep,
    shippingAddress,
    shippingMethod,
    orderPreview,
    isLoading,
    error,
    setShippingAddress,
    setShippingMethod,
    nextStep,
    previousStep,
    goToStep,
    validateAndProceed,
    loadShippingMethods,
    createPreview,
  } = useCheckout();

  const [shippingMethods, setShippingMethods] = useState<ShippingMethod[]>([]);
  const [completedSteps, setCompletedSteps] = useState<CheckoutStep[]>([]);

  // Fetch cart on mount
  useEffect(() => {
    fetchCart();
  }, [fetchCart]);

  // Validate cart when component mounts
  useEffect(() => {
    const validateCart = async () => {
      if (!cart) return;

      const isValid = await validateAndProceed(cart._id);
      if (!isValid) {
        // Redirect to cart if validation fails
        navigate('/cart');
      }
    };

    validateCart();
  }, [cart, validateAndProceed, navigate]);

  // Load shipping methods when reaching shipping method step
  useEffect(() => {
    const loadMethods = async () => {
      if (currentStep === CheckoutStep.SHIPPING_METHOD && shippingMethods.length === 0) {
        const methods = await loadShippingMethods();
        setShippingMethods(methods);
      }
    };

    loadMethods();
  }, [currentStep, shippingMethods.length, loadShippingMethods]);

  // Create order preview when reaching review step
  useEffect(() => {
    const generatePreview = async () => {
      if (currentStep === CheckoutStep.REVIEW && cart && !orderPreview) {
        await createPreview(cart._id);
      }
    };

    generatePreview();
  }, [currentStep, cart, orderPreview, createPreview]);

  // Handle shipping form submission
  const handleShippingSubmit = (address: Partial<Address>) => {
    setShippingAddress(address);
    setCompletedSteps((prev) => [...new Set([...prev, CheckoutStep.SHIPPING_INFO])]);
    nextStep();
  };

  // Handle shipping method selection
  const handleShippingMethodSelect = (method: ShippingMethod) => {
    setShippingMethod(method);
  };

  // Handle continue from shipping method
  const handleShippingMethodContinue = () => {
    if (shippingMethod) {
      setCompletedSteps((prev) => [...new Set([...prev, CheckoutStep.SHIPPING_METHOD])]);
      nextStep();
    }
  };

  // Handle order confirmation (proceed to payment)
  const handleOrderConfirm = () => {
    // For now, just show a message
    // In Phase 6, this will navigate to payment
    alert('Payment integration coming in Phase 6!');
    console.log('Order Preview:', orderPreview);
  };

  // Handle edit shipping address
  const handleEditAddress = () => {
    goToStep(CheckoutStep.SHIPPING_INFO);
  };

  // Handle edit shipping method
  const handleEditShipping = () => {
    goToStep(CheckoutStep.SHIPPING_METHOD);
  };

  // Redirect if cart is empty
  if (cart && cart.item_count === 0) {
    navigate('/cart');
    return null;
  }

  // Loading state
  if (!cart) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Checkout</h1>
        </div>

        {/* Progress Steps */}
        <CheckoutSteps
          currentStep={currentStep}
          completedSteps={completedSteps}
          onStepClick={(step) => {
            if (completedSteps.includes(step)) {
              goToStep(step);
            }
          }}
        />

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {/* Step Content */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          {currentStep === CheckoutStep.SHIPPING_INFO && (
            <ShippingForm
              initialData={shippingAddress || undefined}
              onSubmit={handleShippingSubmit}
              isLoading={isLoading}
            />
          )}

          {currentStep === CheckoutStep.SHIPPING_METHOD && (
            <ShippingMethodSelector
              methods={shippingMethods}
              selectedMethod={shippingMethod}
              onSelect={handleShippingMethodSelect}
              onContinue={handleShippingMethodContinue}
              onBack={previousStep}
              isLoading={isLoading}
            />
          )}

          {currentStep === CheckoutStep.REVIEW && (
            <OrderReview
              cart={cart}
              orderPreview={orderPreview}
              onEditAddress={handleEditAddress}
              onEditShipping={handleEditShipping}
              onConfirm={handleOrderConfirm}
              onBack={previousStep}
              isLoading={isLoading}
            />
          )}

          {currentStep === CheckoutStep.PAYMENT && (
            <div className="text-center py-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Payment</h2>
              <p className="text-gray-600">
                Payment integration will be implemented in Phase 6
              </p>
            </div>
          )}
        </div>

        {/* Cart Summary (Sticky Sidebar on larger screens could go here) */}
      </div>
    </div>
  );
};

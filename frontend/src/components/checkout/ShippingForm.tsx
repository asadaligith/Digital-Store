/**
 * ShippingForm Component
 *
 * Form for collecting shipping address information.
 * Uses controlled inputs with validation.
 */

import React, { useState } from 'react';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { Address, AddressType } from '../../types/address';
import {
  validateRequired,
  validatePhone,
  validatePostalCode,
  validateStateCode,
} from '../../utils/validation';

interface ShippingFormProps {
  initialData?: Partial<Address>;
  onSubmit: (address: Partial<Address>) => void;
  onBack?: () => void;
  isLoading?: boolean;
}

export const ShippingForm: React.FC<ShippingFormProps> = ({
  initialData,
  onSubmit,
  onBack,
  isLoading = false,
}) => {
  const [formData, setFormData] = useState<Partial<Address>>(
    initialData || {
      type: AddressType.SHIPPING,
      country: 'US',
    }
  );

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const handleBlur = (field: string) => {
    setTouched((prev) => ({ ...prev, [field]: true }));
    validateField(field);
  };

  const validateField = (field: string): boolean => {
    const value = formData[field as keyof Address] as string;
    let error = '';

    switch (field) {
      case 'full_name':
      case 'address_line1':
      case 'city':
        if (!validateRequired(value)) {
          error = 'This field is required';
        }
        break;
      case 'state':
        if (!validateRequired(value)) {
          error = 'State is required';
        } else if (!validateStateCode(value)) {
          error = 'Enter 2-letter state code (e.g., NY, CA)';
        }
        break;
      case 'postal_code':
        if (!validateRequired(value)) {
          error = 'Postal code is required';
        } else if (!validatePostalCode(value, formData.country || 'US')) {
          error = 'Enter valid postal code (e.g., 12345)';
        }
        break;
      case 'phone':
        if (!validateRequired(value)) {
          error = 'Phone number is required';
        } else if (!validatePhone(value)) {
          error = 'Enter valid phone number';
        }
        break;
    }

    setErrors((prev) => ({ ...prev, [field]: error }));
    return !error;
  };

  const validateForm = (): boolean => {
    const fields = ['full_name', 'address_line1', 'city', 'state', 'postal_code', 'phone'];
    const newErrors: Record<string, string> = {};
    let isValid = true;

    fields.forEach((field) => {
      const value = formData[field as keyof Address] as string;

      if (!validateRequired(value)) {
        newErrors[field] = 'This field is required';
        isValid = false;
      } else {
        // Additional validation
        switch (field) {
          case 'state':
            if (!validateStateCode(value)) {
              newErrors[field] = 'Enter 2-letter state code';
              isValid = false;
            }
            break;
          case 'postal_code':
            if (!validatePostalCode(value, formData.country || 'US')) {
              newErrors[field] = 'Enter valid postal code';
              isValid = false;
            }
            break;
          case 'phone':
            if (!validatePhone(value)) {
              newErrors[field] = 'Enter valid phone number';
              isValid = false;
            }
            break;
        }
      }
    });

    setErrors(newErrors);
    return isValid;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (validateForm()) {
      onSubmit(formData);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Shipping Information</h2>
        <p className="text-gray-600">Enter your shipping address details</p>
      </div>

      {/* Full Name */}
      <Input
        label="Full Name"
        name="full_name"
        type="text"
        value={formData.full_name || ''}
        onChange={handleChange}
        onBlur={() => handleBlur('full_name')}
        error={touched.full_name ? errors.full_name : undefined}
        required
        placeholder="John Doe"
      />

      {/* Address Line 1 */}
      <Input
        label="Address Line 1"
        name="address_line1"
        type="text"
        value={formData.address_line1 || ''}
        onChange={handleChange}
        onBlur={() => handleBlur('address_line1')}
        error={touched.address_line1 ? errors.address_line1 : undefined}
        required
        placeholder="123 Main St"
      />

      {/* Address Line 2 */}
      <Input
        label="Address Line 2 (Optional)"
        name="address_line2"
        type="text"
        value={formData.address_line2 || ''}
        onChange={handleChange}
        placeholder="Apt 4B, Suite 100, etc."
      />

      {/* City, State, Postal Code Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Input
          label="City"
          name="city"
          type="text"
          value={formData.city || ''}
          onChange={handleChange}
          onBlur={() => handleBlur('city')}
          error={touched.city ? errors.city : undefined}
          required
          placeholder="New York"
        />

        <Input
          label="State"
          name="state"
          type="text"
          value={formData.state || ''}
          onChange={handleChange}
          onBlur={() => handleBlur('state')}
          error={touched.state ? errors.state : undefined}
          required
          placeholder="NY"
          maxLength={2}
        />

        <Input
          label="Postal Code"
          name="postal_code"
          type="text"
          value={formData.postal_code || ''}
          onChange={handleChange}
          onBlur={() => handleBlur('postal_code')}
          error={touched.postal_code ? errors.postal_code : undefined}
          required
          placeholder="10001"
        />
      </div>

      {/* Country */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Country
        </label>
        <select
          name="country"
          value={formData.country || 'US'}
          onChange={handleChange}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
        >
          <option value="US">United States</option>
          <option value="CA">Canada</option>
          <option value="GB">United Kingdom</option>
        </select>
      </div>

      {/* Phone */}
      <Input
        label="Phone Number"
        name="phone"
        type="tel"
        value={formData.phone || ''}
        onChange={handleChange}
        onBlur={() => handleBlur('phone')}
        error={touched.phone ? errors.phone : undefined}
        required
        placeholder="+1-555-123-4567"
      />

      {/* Actions */}
      <div className="flex gap-4 pt-4">
        {onBack && (
          <Button
            type="button"
            variant="outline"
            onClick={onBack}
            disabled={isLoading}
          >
            Back
          </Button>
        )}
        <Button
          type="submit"
          variant="primary"
          fullWidth={!onBack}
          isLoading={isLoading}
        >
          Continue to Shipping Method
        </Button>
      </div>
    </form>
  );
};

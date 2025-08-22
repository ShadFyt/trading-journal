import { z } from 'zod'
import type { AxiosError } from 'axios'

export const NormalizedErrorSchema = z.object({
  type: z.string(),
  message: z.string(),
  status: z.number(),
  code: z.string().optional(),
  fieldErrors: z.record(z.string(), z.array(z.string())).optional(),
})

export type NormalizedError = z.infer<typeof NormalizedErrorSchema>

/**
 * Schema for individual validation error detail
 * Represents a single field validation error from FastAPI/Pydantic
 */
export const validationErrorDetailSchema = z.object({
  type: z.string(),
  loc: z.array(z.string()),
  msg: z.string(),
  input: z.record(z.any()).or(z.string()).optional(),
})

/**
 * Schema for validation error response
 * Array of validation error details
 */
export const validationErrorResponseSchema = z.array(validationErrorDetailSchema)

/**
 * Type definitions
 */
export type ValidationErrorDetail = z.infer<typeof validationErrorDetailSchema>
export type ValidationErrorResponse = z.infer<typeof validationErrorResponseSchema>

/**
 * Convert field names to user-friendly labels
 * @param fieldName - The field name from the API
 * @param fieldLabels - Optional mapping of field names to labels
 * @returns User-friendly field label
 */
const getFieldLabel = (fieldName: string, fieldLabels?: Record<string, string>): string => {
  if (fieldLabels && fieldLabels[fieldName]) {
    return fieldLabels[fieldName]
  }

  // Default: capitalize first letter and convert camelCase to Title Case
  return fieldName
    .replace(/([A-Z])/g, ' $1')
    .replace(/^./, (str) => str.toUpperCase())
    .trim()
}

/**
 * Format validation errors with user-friendly field names
 * @param errors - Array of validation error details
 * @param fieldLabels - Optional mapping of field names to custom labels
 * @returns Formatted error message string with friendly field names
 */
export const formatValidationErrorsWithLabels = (
  errors: ValidationErrorResponse,
  fieldLabels?: Record<string, string>,
): string => {
  return errors
    .map((error) => {
      const field = error.loc.slice(1).join('.')
      const label = getFieldLabel(field, fieldLabels)
      return `${label}: ${error.msg}`
    })
    .join(', ')
}

/**
 * Helper function to get field-specific errors
 * @param errors - Array of validation error details
 * @param fieldName - Name of the field to get errors for
 * @returns Array of error messages for the specific field
 */
export const getFieldErrors = (errors: ValidationErrorResponse, fieldName: string): string[] => {
  return errors
    .filter((error) => {
      const field = error.loc.slice(1).join('.')
      return field === fieldName
    })
    .map((error) => error.msg)
}

/**
 * Parse Axios error into a normalized ApiError object
 * @param error - The Axios error object
 * @returns Normalized ApiError object
 */
export const parseApiError = (
  error: AxiosError<{ detail?: ValidationErrorResponse }, any>,
): NormalizedError => {
  // Network error (no response received)
  if (!error.response) {
    if (error.code === 'ECONNABORTED') {
      return {
        type: 'timeout',
        message: 'Request timed out. Please try again later.',
        status: 504,
      }
    }

    return {
      type: 'network',
      message: 'Network error. Please check your connection and try again.',
      code: error.code,
      status: 500,
    }
  }

  const { status, data } = error.response

  // Authentication error
  if (status === 401 || status === 403) {
    return {
      type: 'auth',
      message: 'Authentication failed. Please log in again.',
      status,
    }
  }

  // Validation error (from FastAPI/Pydantic)
  if (status === 422 && data?.detail) {
    try {
      const validationErrors = validationErrorResponseSchema.parse(data.detail)
      const fieldErrors: Record<string, string[]> = {}
      validationErrors.forEach((error) => {
        const field = error.loc.slice(1).join('.')
        if (!fieldErrors[field]) {
          fieldErrors[field] = []
        }
        fieldErrors[field].push(error.msg)
      })

      return {
        type: 'validation',
        message: 'Validation failed. Please check your input.',
        fieldErrors,
        status,
      }
    } catch {
      // If parsing fails, fall back to generic error
      return {
        type: 'server',
        message: 'Validation error occurred',
        status: 500,
      }
    }
  }

  // Server error
  if (status >= 500) {
    return {
      type: 'server',
      message: 'Server error. Please try again later.',
      status,
    }
  }

  // Generic server error for other HTTP errors
  return {
    type: 'server',
    message: `HTTP error occurred: ${status}`,
    status,
  }
}

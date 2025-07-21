import { z } from 'zod'

/**
 * Schema for individual validation error detail
 * Represents a single field validation error from FastAPI/Pydantic
 */
export const validationErrorDetailSchema = z.object({
  type: z.string(),
  loc: z.array(z.string()),
  msg: z.string(),
  input: z.record(z.any()).optional(),
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

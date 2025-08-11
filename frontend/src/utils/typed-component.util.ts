import type { DefineComponent } from 'vue'
import DateField from '@/components/fields/DateField.vue'
import type { FormActions, GenericObject } from 'vee-validate'

export type DateFieldProps<T extends GenericObject> = {
  name: Extract<keyof T, string>
  title: string
  setFieldValue: FormActions<T>['setFieldValue']
}

export const typedDateField = <T extends GenericObject>() =>
  DateField as unknown as DefineComponent<DateFieldProps<T>>

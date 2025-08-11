<script lang="ts" setup>
import { Icon } from '@iconify/vue'
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { cn } from '@/lib/utils'
import {
  DateFormatter,
  getLocalTimeZone,
  parseDate,
  today,
  CalendarDate,
} from '@internationalized/date'
import type { FormActions } from 'vee-validate'
import type { GenericObject } from 'vee-validate'

defineProps<{
  name: string
  title: string
  setFieldValue: FormActions<GenericObject>['setFieldValue']
}>()

const df = new DateFormatter('en-US', {
  dateStyle: 'long',
})
</script>

<template>
  <FormField :name="name" v-slot="{ value }">
    <FormItem class="flex flex-col">
      <FormLabel class="block text-sm font-medium text-gray-700">{{ title }}</FormLabel>
      <Popover>
        <PopoverTrigger as-child>
          <FormControl>
            <Button
              variant="outline"
              :class="cn('ps-3 text-start font-normal', 'text-muted-foreground')"
            >
              <span>{{ value ? df.format(new Date(value)) : 'Pick a date' }}</span>
              <Icon icon="lucide:calendar-days" width="24" height="24" />
            </Button>
            <input hidden />
          </FormControl>
        </PopoverTrigger>
        <PopoverContent class="w-auto p-0">
          <Calendar
            :model-value="
              value ? parseDate(new Date(value).toISOString().split('T')[0]) : undefined
            "
            :calendar-label="name"
            initial-focus
            :min-value="new CalendarDate(1900, 1, 1)"
            :max-value="today(getLocalTimeZone())"
            @update:model-value="
              (v) => {
                if (v) {
                  setFieldValue(name, v.toDate(getLocalTimeZone()))
                } else {
                  setFieldValue(name, undefined)
                }
              }
            "
          />
        </PopoverContent>
      </Popover>
      <FormMessage />
    </FormItem>
  </FormField>
</template>

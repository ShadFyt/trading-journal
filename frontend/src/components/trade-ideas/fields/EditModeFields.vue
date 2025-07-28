<script setup lang="ts">
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import type { FormActions } from 'vee-validate'

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { Calendar } from '@/components/ui/calendar'
import { cn } from '@/lib/utils'
import { statusOptions } from '@/shared/status'
import {
  CalendarDate,
  DateFormatter,
  getLocalTimeZone,
  parseDate,
  today,
} from '@internationalized/date'
import type { TradeIdeaFormValues } from '@/interfaces/trade-idea.type'

interface Props {
  setFieldValue: FormActions<TradeIdeaFormValues>['setFieldValue']
  isFieldDirty: boolean
  isLiveTrade: boolean
}

const { setFieldValue, isFieldDirty, isLiveTrade } = defineProps<Props>()

const df = new DateFormatter('en-US', {
  dateStyle: 'long',
})
</script>

<template>
  <div class="col-span-4">
    <FormField v-slot="{ componentField }" name="status" :validate-on-blur="!isFieldDirty">
      <FormItem>
        <FormLabel for="status" class="block text-sm font-medium text-gray-700">Status</FormLabel>
        <Select v-bind="componentField" :disabled="isLiveTrade">
          <FormControl>
            <SelectTrigger class="w-full">
              <SelectValue placeholder="Select a status" />
            </SelectTrigger>
          </FormControl>
          <SelectContent>
            <SelectItem v-for="option in statusOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </SelectItem>
          </SelectContent>
        </Select>
        <FormMessage />
      </FormItem>
    </FormField>
  </div>
  <div class="col-span-2">
    <FormField name="ideaDate" v-slot="{ value }">
      <FormItem class="flex flex-col">
        <FormLabel>Idea Date</FormLabel>
        <Popover>
          <PopoverTrigger as-child>
            <FormControl>
              <Button
                variant="outline"
                :class="cn('ps-3 text-start font-normal', 'text-muted-foreground')"
              >
                <span>{{ value ? df.format(new Date(value)) : 'Pick a date' }}</span>
                <CalendarIcon class="ms-auto h-4 w-4 opacity-50" />
              </Button>
              <input hidden />
            </FormControl>
          </PopoverTrigger>
          <PopoverContent class="w-auto p-0">
            <Calendar
              :model-value="
                value ? parseDate(new Date(value).toISOString().split('T')[0]) : undefined
              "
              calendar-label="ideaDate"
              initial-focus
              :min-value="new CalendarDate(1900, 1, 1)"
              :max-value="today(getLocalTimeZone())"
              @update:model-value="
                (v) => {
                  if (v) {
                    setFieldValue('ideaDate', v.toDate(getLocalTimeZone()))
                  }
                }
              "
            />
          </PopoverContent>
        </Popover>
        <FormMessage />
      </FormItem>
    </FormField>
  </div>
</template>

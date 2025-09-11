import { createAnnotation } from '@/api/annotation.api'
import type { AnnotationCreate } from '@/interfaces'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { toast } from 'vue-sonner'
import { AxiosError } from 'axios'
import { liveTradeKeys } from '@/composables/useTradeService.ts'

export const annotationKeys = {
  all: ['annotations'] as const,
  list: () => [...annotationKeys.all, 'list'] as const,
}

export const useAnnotationMutationService = () => {
  const queryClient = useQueryClient()
  const createMutation = useMutation({
    mutationFn: (data: AnnotationCreate) => createAnnotation(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: annotationKeys.list() })
      queryClient.invalidateQueries({ queryKey: liveTradeKeys.list() })
      toast.success('Annotation created successfully')
    },
    onError: (error: unknown) => {
      if (error instanceof AxiosError) {
        const errorMessage = error.response?.data?.message || error.message || 'An error occurred'
        toast.error(`Failed to create annotation: ${errorMessage}`)
      } else {
        toast.error('Failed to create annotation')
      }
    },
  })

  return {
    createMutation,
  }
}

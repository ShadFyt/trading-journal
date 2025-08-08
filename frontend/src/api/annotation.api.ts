import type { Annotation, AnnotationCreate } from '@/interfaces'
import { apiClient } from './client'

const ANNOTATION_API_URL = '/annotations'

export const createAnnotation = (data: AnnotationCreate) => {
  return apiClient.post<Annotation>(ANNOTATION_API_URL, data)
}

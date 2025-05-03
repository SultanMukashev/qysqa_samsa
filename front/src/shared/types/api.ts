export type ApiResponseMessage<T> = {
  ok: boolean,
  data?: T|null,
  message: string
}
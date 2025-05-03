export type LoginRequest = {
  username: string,
  password: string
}

export type LoginResponse = {
  message: string,
  data: {
    id: number,
    firstname: string,
    lastname: string,
    phoneNumber: string,
    role: string,
    city: string,
    gender: string,
    birthDate: string,
  }
}
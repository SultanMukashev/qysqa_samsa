'use client'

import AppForm, { FormField } from "@/shared/components/Form"
import { Toast } from 'primereact/toast';
import { useEffect, useRef } from "react"
import { FieldValues } from "react-hook-form"
import { LoginRequest } from "./api/login/type"
import { useRouter } from "next/navigation"
import { useMe } from "@/shared/store/useMe"

const LogInUI = () => {

  const { fetchMe, isAuth } = useMe()
  const router = useRouter()
  const toast = useRef<Toast>(null)

  useEffect(() => {
    if (isAuth()) {
      router.push('/')
    }
  })

  const fields: FormField[] = [
    {
      name: 'username',
      label: 'Username',
      required: true,
      type: 'text',
      classes: 'col-start-1 col-end-4',
    },
    {
      name: 'password',
      type: 'password',
      label: 'Password',
      required: true,
      classes: 'col-start-1 col-end-4',
    }
  ]

  const onSubmit = async (data: FieldValues) => {
    const res = await fetchMe(data as LoginRequest)
    if (res.ok) {router.push('/'); return}
    toast.current?.show({ severity: 'error', summary: 'Error', detail: res.message });
  }

  return (
    <div className="w-full h-screen flex flex-col items-center justify-center">
      <div className="p-4 w-[350px] border border-neutral-300">
        <AppForm fields={fields} onSubmit={(data) => onSubmit(data)} buttonTitle="Войти" buttonClass="w-[315px]"></AppForm>
      </div>
      <Toast ref={toast}></Toast>
    </div>
  )
}

export default LogInUI
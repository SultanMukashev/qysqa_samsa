'use client'

import AppForm, { FormField } from "@/shared/components/Form"
import { Toast } from 'primereact/toast';
import { useEffect, useRef } from "react"
import { FieldValues } from "react-hook-form"
import { LoginRequest } from "./api/login/type"
import { useRouter } from "next/navigation"
import { useMe } from "@/shared/store/useMe"

import { TabPanel, TabView } from "primereact/tabview";
import { LoginTeacherRequest } from "./api/loginTeacher/type";

const LogInUI = () => {

  const { fetchMeStudent, fetchMeTeacher, isAuth } = useMe()
  const router = useRouter()
  const toast = useRef<Toast>(null)

  useEffect(() => {
    if (isAuth()) {
      router.push('/')
    }
  }, [])
  

  const fieldsStudent: FormField[] = [
    {
      name: 'student_id',
      label: 'Student ID',
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

  const fieldsTeacher: FormField[] = [
    {
      name: 'id',
      label: 'ID',
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

  const onSubmitStudent = async (data: FieldValues) => {
    const res = await fetchMeStudent(data as LoginRequest)
    if (res.ok) {router.push('/'); return}
    toast.current?.show({ severity: 'error', summary: 'Error', detail: res.message });
  }

  const onSubmitTeacher = async (data: FieldValues) => {
    const res = await fetchMeTeacher(data as LoginTeacherRequest)
    if (res.ok) {router.push('/'); return}
    toast.current?.show({ severity: 'error', summary: 'Error', detail: res.message });
  }

  return (
    <div className="w-full h-screen flex flex-col items-center justify-center">
      <TabView>
        <TabPanel header="Student">
          <div className="p-4 w-[350px] border rounded-md border-neutral-300">
            <AppForm fields={fieldsStudent} onSubmit={(data) => onSubmitStudent(data)} buttonTitle="Войти" buttonClass="w-[315px]"></AppForm>
          </div>
        </TabPanel>
        <TabPanel header="Teacher">
          <div className="p-4 w-[350px] border rounded-md border-neutral-300">
            <AppForm fields={fieldsTeacher} onSubmit={(data) => onSubmitTeacher(data)} buttonTitle="Войти" buttonClass="w-[315px]"></AppForm>
          </div>
        </TabPanel>
      </TabView>
      <Toast ref={toast}></Toast>
    </div>
  )
}

export default LogInUI
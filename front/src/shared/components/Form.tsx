'use client'

import React, { useEffect, useMemo, useState } from 'react';
import { useForm, Controller, FieldValues, DefaultValues, Path } from 'react-hook-form';
import { InputText } from 'primereact/inputtext';
import { Dropdown } from 'primereact/dropdown';
import { Calendar } from 'primereact/calendar';
import { Checkbox } from 'primereact/checkbox';
import { RadioButton } from 'primereact/radiobutton';
import { InputTextarea } from 'primereact/inputtextarea';
import { AutoComplete, AutoCompleteCompleteEvent } from 'primereact/autocomplete';
import { MultiSelect } from 'primereact/multiselect';
import { InputMask } from 'primereact/inputmask';

export interface FormField {
  type: 'text' | 'number' | 'email' | 'password' | 'dropdown' | 'textarea' | 'calendar' | 'checkbox' | 'radiobutton' | 'autocomplete' | 'multiselect';
  name: string;
  label: string;
  options?: { label: string; value: string | number }[];
  colStart?: number;
  colEnd?: number;
  required?: boolean;
  classes?: string;
  defaultValue?: unknown;
  mask?: string,
  calendar?: {
    timeOnly?: boolean
  }
  validation?: {
    minLength?: { value: number; message: string };
    maxLength?: { value: number; message: string };
    pattern?: { value: RegExp; message: string };
    custom?: (value: unknown) => string | true;
  };
}

interface FormConfig<T extends FieldValues = FieldValues> {
  fields: FormField[];
  onSubmit: (data: T) => void;
  buttonTitle?: string;
  buttonClass?: string;
  onChange?: (data: T) => void;
}

const AppForm = <T extends FieldValues = FieldValues>({
  fields,
  onSubmit,
  buttonTitle,
  buttonClass,
  onChange
}: FormConfig<T>) => {
  const defaultValues = useMemo(() => {
    return fields.reduce((acc, field) => {
      acc[field.name] = field.defaultValue ?? '';
      return acc;
    }, {} as DefaultValues<T>);
  }, [fields]);

  const [suggestions, setSuggestions] = useState<{ label: string; value: string | number }[]>([]);
  const [autocompleteSource, setAutocompleteSource] = useState<{ label: string; value: string | number }[]>([]);
  
  const {
    control,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<T>({ defaultValues });

  useEffect(() => {
    const subscription = watch((value) => {
      if (onChange) onChange(value as T);
    });
    return () => subscription.unsubscribe();
  }, [watch, onChange]);

  useEffect(() => {
    const autocompleteField = fields.find(f => f.type === 'autocomplete');
    if (autocompleteField?.options) {
      setAutocompleteSource(autocompleteField.options);
      setSuggestions(autocompleteField.options)
    }
  }, [fields]);

  const completeMethod = (event: AutoCompleteCompleteEvent) => {
    if (!event.query) {
      setSuggestions(autocompleteSource);
      return;
    }
  
    const filtered = autocompleteSource.filter((item) =>
      item.label.toLowerCase().includes(event.query.toLowerCase())
    );
    setSuggestions(filtered);
  };    

  const getFormErrorMessage = (name: string) => {
    return errors[name] ? <small className="p-error">{String(errors[name]?.message)}</small> : null;
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="grid grid-cols-3 gap-4">
      {fields.map((field) => {
        const fieldClasses = field.classes || '';
        return (
          <div key={field.name} className={fieldClasses}>
            <label htmlFor={field.name} className="text-sm">{field.label}<span className='text-red-500'>{field.required && ' * '}</span></label>
            <Controller
              name={field.name as keyof T as Path<T>}
              control={control}
              rules={{
                required: field.required ? `${field.label} required` : false,
                minLength: field.validation?.minLength,
                maxLength: field.validation?.maxLength,
                pattern: field.validation?.pattern,
                validate: field.validation?.custom,
              }}
              render={({ field: controllerField }): React.ReactElement => {
                if (['text', 'number', 'email', 'password'].includes(field.type) && !field.mask) {
                  return <InputText id={field.name} type={field.type} className="w-full" {...controllerField} />;
                }
                if (['text', 'number', 'email', 'password'].includes(field.type) && field.mask) {
                  return <InputMask id={field.name} type={field.type} mask={field.mask} className="w-full"  {...controllerField} />;
                }
                if (field.type === 'dropdown') {
                  return (
                    <Dropdown
                      id={field.name}
                      className="w-full"
                      options={field.options}
                      value={controllerField.value}
                      onChange={(e) => controllerField.onChange(e.value)}
                    />
                  );
                }
                if (field.type === 'calendar') {
                  return <Calendar id={field.name} className="w-full" timeOnly={field.calendar?.timeOnly} dateFormat="dd/mm/yy" stepMinute={5} {...controllerField} />;
                }
                if (field.type === 'checkbox') {
                  return (
                    <div className="flex align-items-center">
                      <Checkbox
                        inputId={field.name}
                        checked={controllerField.value}
                        onChange={(e) => controllerField.onChange(e.checked)}
                      />
                      <label htmlFor={field.name} className="ml-2">{field.label}</label>
                    </div>
                  );
                }
                if (field.type === 'radiobutton') {
                  return (
                    <div className="flex align-items-center gap-2">
                      {field.options?.map((option) => (
                        <div key={option.value} className="flex align-items-center gap-2">
                          <RadioButton
                            inputId={String(option.value)}
                            name={field.name}
                            value={option.value}
                            checked={controllerField.value === option.value}
                            onChange={(e) => controllerField.onChange(e.value)}
                          />
                          <label htmlFor={String(option.value)}>{option.label}</label>
                        </div>
                      ))}
                    </div>
                  )
                }
                if (field.type === 'textarea') {
                  return (
                    <div className="w-full">
                      <InputTextarea id={field.name} className="w-full p-0" {...controllerField} />
                    </div>
                  );
                }
                if (field.type === 'autocomplete') {
                  return (
                    <div className="w-full">
                      <AutoComplete<{ label: string; value: string | number }[]>
                        className="w-full"
                        suggestions={suggestions}
                        completeMethod={completeMethod}
                        field="label"
                        value={controllerField.value}
                        onChange={(e) => controllerField.onChange(e.value)}
                      />
                    </div>
                  );
                }
                if (field.type === 'multiselect') {
                  return (
                    <div className='w-full'>
                      <MultiSelect
                        className='w-full'
                        display='chip'
                        optionLabel='label'
                        optionValue='value'
                        options={field.options}
                        {...controllerField}
                      />
                    </div>
                  )
                }
                return <></>
              }}
            />
            {getFormErrorMessage(field.name)}
          </div>
        );
      })}

        <div className="col-span-3 grid grid-cols-subgrid gap-4">
          <button
            type="submit"
            className={`${buttonClass ? buttonClass : 'col-start-3 w-[150px] justify-self-end'} p-2 border text-neutral-500 border-neutral-500 rounded-sm text-sm`}
          >
            {buttonTitle ? buttonTitle : 'Отправить'}
          </button>
        </div>
    </form>
  );
};

export default AppForm;

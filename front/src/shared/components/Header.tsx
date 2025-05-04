import { useMe } from "../store/useMe"

const HeaderUI = () => {
  const { me } = useMe()

  return (
    <header className="flex h-[50px] border-b-1 shadow-md shadow-neutral-100/50 border-neutral-200 w-full items-center px-6 justify-between">
      <div className="text-md font-bold">
        Qysqa Snap
      </div>
      <div>
        <div className="w-[40px] h-[40px] flex flex-row items-center justify-center font-medium text-white text-sm rounded-full bg-sky-500">
          {`${me?.name.slice(0, 1).toUpperCase()}${me?.surname.slice(0, 1).toUpperCase()}`}
        </div>
      </div>
    </header>
  )
}

export default HeaderUI
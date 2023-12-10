// import {useAsync} from "react-use";
import useSWR from "swr";
import {useInitData} from "@vkruglikov/react-telegram-web-app";
import type {InitDataUnsafe} from "@vkruglikov/react-telegram-web-app";


export function useSafeInitData() {
  const [, initData] = useInitData();
  // const initData = window.Telegram.WebApp.initData;
  // console.log(initData);

  return useSWR<InitDataUnsafe>(`${import.meta.env.VITE_API_BASE_URL}/validate_init_data?${initData}`, async (url: string) => {
    const response = await fetch(url);
    return await response.json() as InitDataUnsafe;
  });

  // return useAsync<() => Promise<InitDataUnsafe>>(async () => {
  //   const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/validate_init_data?${initData}`);
  //   return await response.json() as InitDataUnsafe;
  // }, [initData]);
}

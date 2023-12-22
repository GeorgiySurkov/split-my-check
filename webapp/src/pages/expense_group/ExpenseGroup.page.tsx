import React from "react";
import WebApp from "@twa-dev/sdk";
import {ExpenseList} from "src/entities/expense";
import {useSafeTgInitData} from "src/shared/lib/safe_tg_init_data";
import {MainButton} from "@twa-dev/sdk/react";


export const ExpenseGroupPage: React.FC = () => {
  const initData = useSafeTgInitData();

  const onMainButtonCLick = React.useCallback(() => {
    WebApp.showAlert("Вот это да");
  }, []);

  const prettyTgData = JSON.stringify(initData, null, 2);

  return (
    <div style={{color: "var(--tg-theme-text-color)"}}>
      <h1 style={{color: "var(--tg-theme-text-color)"}}>ExpenseGroupPage</h1>
      {prettyTgData}
      <MainButton text="Волшебство" onClick={onMainButtonCLick}/>
      <ExpenseList/>
    </div>
  )
}

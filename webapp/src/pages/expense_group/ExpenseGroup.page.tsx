import React from "react";

import {MainButton} from "@twa-dev/sdk/react";
import {useNavigate} from "react-router-dom";

import {ExpenseList} from "src/entities/expense";
import {useSafeTgInitData} from "src/shared/lib/safe_tg_init_data";


export const ExpenseGroupPage: React.FC = () => {
  const navigate = useNavigate();

  const initData = useSafeTgInitData();

  const onMainButtonCLick = React.useCallback(() => {
    // WebApp.showAlert("Вот это да");
    navigate("/edit");
  }, [navigate]);

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

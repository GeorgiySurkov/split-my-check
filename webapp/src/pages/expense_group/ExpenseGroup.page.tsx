import React from "react";
import {MainButton, useWebApp} from "@vkruglikov/react-telegram-web-app";
import {ExpenseList} from "src/entities/expense";
import {useSafeTgInitData} from "src/shared/lib/safe_tg_init_data";


export const ExpenseGroupPage: React.FC = () => {
    // const [InitData, initDataStr] = useInitData();
    const initData = useSafeTgInitData();

    const {showAlert} = useWebApp();
    const onMainButtonCLick = React.useCallback(() => {
        showAlert("Вот это да");
    }, [showAlert]);

    const prettyTgData = JSON.stringify(initData, null, 2);

    return (
        <div>
            <h1>ExpenseGroupPage</h1>
            {prettyTgData}
            <MainButton text="Волшебство" onClick={onMainButtonCLick}/>
            <ExpenseList/>
        </div>
    )
}

import React from "react";
import {MainButton, useWebApp} from "@vkruglikov/react-telegram-web-app";
import {ExpenseList} from "src/entities/expense";
import {useSafeInitData} from "src/shared/lib/tg_validation";


export const ExpenseGroupPage: React.FC = () => {
    // const [InitData, initDataStr] = useInitData();
    const {isLoading: loading, data: value, error} = useSafeInitData();

    const {showAlert} = useWebApp();
    const onMainButtonCLick = React.useCallback(() => {
        showAlert("Вот это да");
    }, [showAlert]);

    if (loading) {
        return <div>Loading...</div>
    }
    if (error) {
        const prettyError = JSON.stringify(error, null, 2);
        return <div>Error: {prettyError}</div>
    }

    const prettyTgData = JSON.stringify(value, null, 2);

    return (
        <div>
            <h1>ExpenseGroupPage</h1>
            {prettyTgData}
            <MainButton text="Волшебство" onClick={onMainButtonCLick}/>
            <ExpenseList/>
        </div>
    )
}

import React from "react";

import {BackButton} from "@twa-dev/sdk/react";
import {useNavigate} from "react-router-dom";


export const TgRoutingBackButton: React.FC = () => {
    const navigate = useNavigate();

    const onBackButtonClick = React.useCallback(() => {
      navigate(-1);
    }, [navigate]);

    return <BackButton onClick={onBackButtonClick} />;
}

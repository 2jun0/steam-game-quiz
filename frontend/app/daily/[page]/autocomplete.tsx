import React, { useState } from "react";
import {Autocomplete, AutocompleteItem, MenuTriggerAction} from "@nextui-org/react";
import { autoCompleteGameName } from "@/utils/backend-api";

type CompleteName = {
    name: string
}

type FieldState = {
  selectedKey: React.Key | null;
  inputValue: string;
  items: Array<CompleteName>;
};

export default function AutoCompleteGameName({onChangeGuessName}: {onChangeGuessName: (_:string) => void}) {
    const [autoCompleteNames, setAutoCompleteNames] = useState<Array<CompleteName>>([]);

    // Store Autocomplete input value, selected option, open state, and items
    // in a state tracker
    const [fieldState, setFieldState] = useState<FieldState>({
        selectedKey: "",
        inputValue: "",
        items: autoCompleteNames,
    }, );

    // Specify how each of the Autocomplete values should change when an
    // option is selected from the list box
    const onSelectionChange = (key: React.Key) => {
        setFieldState((prevState) => {
            let selectedItem = prevState.items.find((option) => option.name === key);

            return {
                inputValue: selectedItem?.name || "",
                selectedKey: key,
                items: autoCompleteNames,
            };
        });

        onChangeGuessName(key.toString());
    };

    // Specify how each of the Autocomplete values should change when the input
    // field is altered by the user
    const onInputChange = async (value: string) => {
        const _autoCompleteNames = await autoCompleteGameName(value) as Array<CompleteName>
        setAutoCompleteNames(_autoCompleteNames)
        setFieldState((prevState) => ({
            inputValue: value,
            selectedKey: value === "" ? null : prevState.selectedKey,
            items: _autoCompleteNames,
        }));

        onChangeGuessName(value)
    };

  // Show entire list if user opens the menu manually
  const onOpenChange = (isOpen: boolean, menuTrigger: MenuTriggerAction) => {
        if (menuTrigger === "manual" && isOpen) {
            setFieldState((prevState) => ({
                inputValue: prevState.inputValue,
                selectedKey: prevState.selectedKey,
                items: autoCompleteNames,
            }));
        }
  };

  return (
    <Autocomplete
        className="w-full"
        variant="bordered"
        label="Enter your guess here" 
        inputValue={fieldState.inputValue}
        items={fieldState.items}
        selectedKey={fieldState.selectedKey}
        onInputChange={onInputChange}
        onOpenChange={onOpenChange}
        onSelectionChange={onSelectionChange}
        onKeyDown={(e: any) => e.continuePropagation()}
    >
        {(item) => <AutocompleteItem key={item.name}>{item.name}</AutocompleteItem>}
    </Autocomplete>
  );
}

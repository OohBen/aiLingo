import { Language } from "../types";

type LanguageListProps = {
  languages: Language[];
};

export function LanguageList({ languages }: LanguageListProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {languages.map((language) => (
        <div key={language.id} className="bg-gray-300 shadow-md rounded-lg p-4">
          <h2 className="text-xl font-semibold mb-2 text-black">
            {language.name}
          </h2>
          <p className="text-black">{language.description}</p>
        </div>
      ))}
    </div>
  );
}

import { getLanguages } from '../../lib/api';
import { LanguageList } from '../../components/LanguageList';

export default async function Languages() {
  const languages = await getLanguages();

  return (
    <div>
      <h1>Languages</h1>
      <LanguageList languages={languages} />
    </div>
  );
}
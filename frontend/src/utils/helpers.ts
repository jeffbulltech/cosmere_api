import { 
  Character, Book, World, MagicSystem, Shard,
  ParsedCharacter, ParsedBook, ParsedWorld, ParsedMagicSystem, ParsedShard
} from '../types/cosmere';

/**
 * Safely parse JSON string, returning null if parsing fails
 */
export function safeJsonParse<T>(jsonString: string | null | undefined): T | null {
  if (!jsonString) return null;
  try {
    return JSON.parse(jsonString);
  } catch (error) {
    console.warn('Failed to parse JSON string:', jsonString, error);
    return null;
  }
}

/**
 * Convert a Character with JSON strings to a ParsedCharacter with objects
 */
export function parseCharacter(character: Character): ParsedCharacter {
  return {
    ...character,
    aliases: safeJsonParse<string[]>(character.aliases),
    magic_abilities: safeJsonParse<Record<string, any>>(character.magic_abilities),
    affiliations: safeJsonParse<Record<string, any>>(character.affiliations),
    cosmere_significance: safeJsonParse<Record<string, any>>(character.cosmere_significance),
  };
}

/**
 * Convert a Book with JSON strings to a ParsedBook with objects
 */
export function parseBook(book: Book): ParsedBook {
  return {
    ...book,
    cosmere_significance: safeJsonParse<Record<string, any>>(book.cosmere_significance),
  };
}

/**
 * Convert a World with JSON strings to a ParsedWorld with objects
 */
export function parseWorld(world: World): ParsedWorld {
  return {
    ...world,
    geography: safeJsonParse<Record<string, any>>(world.geography),
  };
}

/**
 * Convert a MagicSystem with JSON strings to a ParsedMagicSystem with objects
 */
export function parseMagicSystem(magicSystem: MagicSystem): ParsedMagicSystem {
  return {
    ...magicSystem,
    mechanics: safeJsonParse<Record<string, any>>(magicSystem.mechanics),
    limitations: safeJsonParse<Record<string, any>>(magicSystem.limitations),
  };
}

/**
 * Convert a Shard with JSON strings to a ParsedShard with objects
 */
export function parseShard(shard: Shard): ParsedShard {
  return {
    ...shard,
    splinter_info: safeJsonParse<Record<string, any>>(shard.splinter_info),
  };
}

/**
 * Format a date string for display
 */
export function formatDate(dateString: string | null | undefined): string {
  if (!dateString) return 'Unknown';
  try {
    return new Date(dateString).toLocaleDateString();
  } catch (error) {
    return 'Invalid Date';
  }
}

/**
 * Truncate text to a specified length
 */
export function truncateText(text: string | null | undefined, maxLength: number = 100): string {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}

/**
 * Capitalize first letter of each word
 */
export function capitalizeWords(text: string): string {
  return text.replace(/\b\w/g, (char) => char.toUpperCase());
}

/**
 * Get status color for character status
 */
export function getStatusColor(status: string | null | undefined): string {
  switch (status?.toLowerCase()) {
    case 'alive':
      return 'text-green-600 bg-green-100';
    case 'dead':
      return 'text-red-600 bg-red-100';
    case 'cognitive_shadow':
      return 'text-purple-600 bg-purple-100';
    default:
      return 'text-gray-600 bg-gray-100';
  }
}

/**
 * Get status display text
 */
export function getStatusDisplay(status: string | null | undefined): string {
  switch (status?.toLowerCase()) {
    case 'alive':
      return 'Alive';
    case 'dead':
      return 'Dead';
    case 'cognitive_shadow':
      return 'Cognitive Shadow';
    default:
      return 'Unknown';
  }
}

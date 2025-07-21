# Cosmere Frontend

A modern React application for exploring Brandon Sanderson's Cosmere universe. This frontend provides an intuitive interface for browsing characters, worlds, books, and magic systems from the Cosmere.

## 🚀 Features

- **Character Explorer**: Browse and search characters with detailed information
- **World Maps**: Interactive maps and information about Cosmere worlds
- **Book Database**: Complete catalog of Cosmere books with reading order
- **Magic Systems**: Detailed information about various magic systems
- **Advanced Search**: Full-text search across all content
- **Relationship Visualization**: Character connections and relationships
- **Timeline**: Chronological events across the Cosmere
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🛠️ Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **React Query** for server state management
- **React Router** for navigation
- **Axios** for API communication
- **Headless UI** for accessible components
- **Heroicons** for icons
- **Recharts & D3** for data visualizations

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cosmere-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   ```
   Edit `.env.local` and set your configuration:
   ```env
   REACT_APP_API_URL=http://localhost:5240/api/v1
   ```

4. **Start the development server**
   ```bash
   npm start
   ```

The application will be available at `http://localhost:3000`

## 🏗️ Project Structure

```
src/
├── components/          # React components
│   ├── common/         # Shared components (Header, Footer, etc.)
│   ├── books/          # Book-related components
│   ├── characters/     # Character components
│   └── worlds/         # World components
├── pages/              # Page components
├── hooks/              # Custom React hooks
├── services/           # API and external services
├── types/              # TypeScript type definitions
├── utils/              # Utility functions
├── styles/             # Styling files
├── contexts/           # React contexts
└── layouts/            # Layout components
```

## 🎨 Styling

This project uses **Tailwind CSS** with custom theme configuration:

- **Custom Colors**: Cosmere-themed color palette
- **Custom Fonts**: Inter for UI, Georgia for headings
- **Custom Components**: Pre-built component classes
- **Responsive Design**: Mobile-first approach

### Custom Color Palette

- `cosmere-*`: Primary brand colors
- `roshar-*`: Roshar-themed colors
- `scadrial-*`: Scadrial-themed colors

## 🔧 Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint errors
- `npm run type-check` - Run TypeScript type checking

## 🌐 API Integration

The frontend communicates with the Cosmere API backend. Key API endpoints:

- `/api/v1/characters` - Character management
- `/api/v1/books` - Book information
- `/api/v1/worlds` - World data
- `/api/v1/magic-systems` - Magic system details
- `/api/v1/search` - Search functionality

## 📱 Responsive Design

The application is fully responsive and optimized for:
- **Desktop**: Full-featured experience
- **Tablet**: Touch-optimized interface
- **Mobile**: Streamlined mobile experience

## 🧪 Testing

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage
```

## 🚀 Deployment

### Production Build

```bash
npm run build
```

### Environment Variables for Production

Set the following environment variables in your production environment:

```env
REACT_APP_API_URL=https://api.cosmere-api.com/api/v1
REACT_APP_ENVIRONMENT=production
REACT_APP_DEBUG=false
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Brandon Sanderson** for creating the amazing Cosmere universe
- **Coppermind Wiki** for reference material
- **17th Shard** community for insights and discussions

## 📞 Support

For support, please open an issue in the GitHub repository or contact the development team.

---

**Journey before destination, Radiant.** 
# Web-Based TODO Application - Frontend

Next.js frontend for the TODO application.

## Setup

1. Install dependencies:
```bash
npm install
```

## Running the Application

Start the development server:
```bash
npm run dev
```

The application will be available at http://localhost:3000

## Building for Production

Build the application:
```bash
npm run build
```

Start the production server:
```bash
npm start
```

## Features

- View all tasks with completion status
- Add new tasks
- Mark tasks as complete
- Edit task descriptions
- Delete tasks
- Persistent storage (tasks saved on backend)

## Project Structure

```
frontend/
├── src/
│   ├── app/             # Next.js app directory
│   │   ├── page.tsx     # Main page
│   │   ├── layout.tsx   # Root layout
│   │   └── globals.css  # Global styles
│   ├── components/      # React components
│   ├── services/        # API client
│   └── types/           # TypeScript types
├── public/              # Static assets
└── package.json         # Dependencies
```

## Environment Variables

Create a `.env.local` file to configure the API URL:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Testing

Run tests:
```bash
npm test
```

## Technologies

- Next.js 14+ (App Router)
- React 18+
- TypeScript
- CSS (no framework)

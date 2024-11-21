# How the Frontend Works

If you would like to contribute to frontend components, this document might be of help to you!
The files listed below are components that you will most likely have to interact with.
We assme that the file path will be repo_name/frontend/src/ etc.

## src/

### App.css
This is the file that holds a majority of our CSS styling. The styling is broken down by components (for the most part).
If you would like to create a new component, we suggest you put your styling in this css file. Or, you can make your own css
styling file -- just make sure to import it in the correct places.

### App.tsx
This is the component that gets called my our main typescript file. It holds calls to child components:
- Navbar
- Banner
- Footer

### Index.css
This is the syling that applies to the entire webpage; it's the top of the CSS hierarchy. This has information on how 
the body and h1 tags are styled.

### main.tsx
This component is the head of the web-app. It calls the App component.

## src/components
### Banner.tsx
This is the component that holds a majority of our logic.  It basically houses the body of the application.
It is in charge of handling user input via the search bar and search button, running the backend script, displaying
song rows, displaying song cards, playing music, etc.

### Footer.tsx
Holds our footer space with links to documentation, contributing guidelines, etc.

### MainSongCard.tsx
This is the component that creates a large song card for the song that the user searched up. 
Input: {song_name, artist, album_cover, preview_url, link_url}. 
```
Type: type SongCardProps = {
    song_name: string;
    artist: string;
    album_cover: string;
    preview_url: string;
    link_url: string;
}
```

### Navbar.tsx
Very simple navbar which holds a link to the github repo.

### SongCard.tsx
This is the component that creates an individual song card. Similar to the MainSongCard, but smaller.
Input: {song_name, artist, album_cover, preview_url, link_url}. 
```
Type: type SongCardProps = {
    song_name: string;
    artist: string;
    album_cover: string;
    preview_url: string;
    link_url: string;
}
```

### SongRows.tsx
This is a component that builds up the return object to the Banner.tsx file. It creates 9 different song cards,
1 main song card, and 8 individual song cards. i.e., calls MainSongCard.tsx x1, SongCard.tsx x8.
Input: {song_name, artist, album_cover, preview_url, link_url}. An array of song information, sourced from the backend file (in the form of a JSON).
```
Type: type SongCardProps = {
    song_name: string;
    artist: string;
    album_cover: string;
    preview_url: string;
    link_url: string;
}
```

## src/assets
This is home to all of the images that we used for the project. If you would like to add any static images, please
place them in this folder.

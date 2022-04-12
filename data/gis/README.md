

## Field Definitions

<dl>
    <dt>accuracy_assessment_uri</dt>
    <dd>
        <ul>
            <li>A Uniform Resource Identifier for an HTML document that describes the source, precision, and accuracy of the coordinates provided for a particular location.</li>
            <li>Applies to: locations.csv</li>
        </ul>
    </dd>
    <dt>accuracy_radius</dt>
    <dd>
        <ul>
            <li>Distance in meters indicating the presumed horizontal accuracy of the coordinates provided for a particular location.</li>
            <li>Applies to: locations.csv</li>
        </ul>
    </dd>
    <dt>archaeological_remains</dt>
    <dd>
        <ul>
            <li>Term indicating whether archaeological remains are known to be visible at a particular location and, if so, how substantive they are.</li>
            <li>Terms and definitions: archaeological_remains.csv</li>
            <li>Applies to: locations.csv</li>
        </ul>
    </dd>
    <dt>association_certainty</dt>
    <dd>
        <ul>
            <li>Term indicating the level of certainty in the association between a place and a name, location, or connection.</li>
            <li>Terms and definitions: association_certainty.csv</li>
            <li>Applies to: connections.csv, locations_*.csv, names.csv.</li>
        </ul>
    </dd>
    <dt>attested_form</dt>
        <ul>
            <li>Transcription of the attested form of the name in its original language and script (Unicode characters), if known.</li>
            <li>Applies to: names.csv</li>
        </ul>
    <dd></dd>
    <dt>bounding_box_wkt</dt>
        <ul>
            <li>A bounding box for the geometries of all locations associated with a given place.</li>
            <li>Format: expressed as a Polygon using the [Well-Known Text (WKT)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) format.</li>
        </ul>
    <dd></dd>
    <dt>connection_type</dt>
    <dd>
        <ul>
            <li>Term indicating the nature of a connection between two places.</li>
            <li>Terms and definitions: connection_types.csv</li>
            <li>Applies to: connections.csv.</li>
        </ul>
    </dd>
    <dt>connects_to</dt>
    <dd>
        <ul>
            <li>Uniform Resource Identifier of the Pleiades place that is the object of a connection.</li>
            <li>Applies to: connections.csv.</li>
        </ul>    
    </dd>
    <dt>created</dt>
    <dd>
        <ul>
            <li>Date and time the record was created in the Pleiades gazetteer.</li>
            <li>Format: A date-time string conforming to the [ISO 8601 Date and Time Format](https://en.wikipedia.org/wiki/ISO_8601), e.g. "2016-07-13T13:31:46Z". All date-times are calculated to the second in Universal Coordinated Time (UTC) and the "Z" timezone indicator is appended.</li>
            <li>Applies to: connections.csv, locations_*.csv, names.csv, and places.csv.</li>
        </ul>
    </dd>
    <dt>description</dt>
    <dd>
        <ul>
            <li>A English-language description of a particular connection, location, name, or place.</li>
            <li>Applies to: connections.csv, locations_*.csv, names.csv, and places.csv.</li>
        </ul>
    </dd>
    <dt>details</dt>
    <dd>
        <ul>
            <li>English-language text providing discussion of a particular connection, location, name, or place above and beyond that included in the "description".</li>
            <li>Format: This field may include HTML tags.</li>
            <li>Applies to: connections.csv, locations_*.csv, names.csv, and places.csv.</li>
        </ul>
    </dd>
    <dt>geometry_wkt</dt>
    <dd>
        <ul>
            <li>Spatial geometry of a particular location.</li>
            <li>Applies to: locations_*.csv.</li>
        </ul>
    </dd>
    <dt>id</dt>
    <dd>
        <ul>
            <li>Alphanumeric identifier for a particular connection, name, location, or place. Can be used together with "place_id" to join connections, names, and locations with the corresponding place data.</li>
            <li>Note: A given "id" value is unique within the CSV file in which is appears; however, "id" uniqueness in the Pleiades webapp is contextual. Therefore, to obtain a completely unique identifier for any item in the Pleiades dataset, use its "uri" value rather than its "id" value.
            <li>Applies to: connections.csv, locations_*.csv, names.csv, and places.csv.</li>
        </ul>
    </dd>
    <dt>language_tag</dt>
    <dd>
        <ul>
            <li>An alphabetic string indicating the language and writing system of the name contained in the "attested_form" field.</li>
            <li>Format: A string conforming to [IETF BCP 47 Language Tags](https://tools.ietf.org/rfc/bcp/bcp47.txt) whose subtags are registered in the [IANA Language Subtag Registry](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry).</li>
            <li>Terms and definitions: all language tags appearing in Pleiades data are defined in languages_and_scripts.csv.</li>
            <li>Applies to: names.csv.</li>
        </ul>
    </dd>
    <dt>name_type</dt>
    <dd></dd>
    <dt>place_id</dt>
    <dd></dd>
    <dt>provenance</dt>
    <dd></dd>
    <dt>representative_latitude</dt>
    <dd></dd>
    <dt>representative_longitude</dt>
    <dd></dd>
    <dt>romanized_form_1</dt>
    <dd></dd>
    <dt>romanized_form_2</dt>
    <dd></dd>
    <dt>romanized_form_3</dt>
    <dd></dd>
    <dt>title</dt>
    <dd></dd>
    <dt>transcription_accuracy</dt>
    <dd></dd>
    <dt>transcription_completeness</dt>
    <dd></dd>
    <dt>uri</dt>
    <dd></dd>
    <dt>year_after_which</dt>
    <dd></dd>
    <dt>year_before_which</dt>
    <dd></dd>

</dl>

## Field Coverage

| heading | places | names | locations | connections |
| --- |:---:|:---:|:---:|:---:|
| created | x | x | x | x |